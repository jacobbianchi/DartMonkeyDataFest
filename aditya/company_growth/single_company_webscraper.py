from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import time
import pickle

# Set up Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")  # Reduce bot detection
options.add_argument("--disable-dev-shm-usage")  # Prevent resource issues
options.add_argument("--no-sandbox")  # Bypass OS security model
options.add_argument("start-maximized")  # Maximize window for human-like behavior
driver = webdriver.Chrome(options=options)

try:
    # Hide Selenium's automation footprint
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """
    })

    # Load the page
    url = "https://www.crunchbase.com/organization/capital-investment-advisors"
    driver.get(url)

    # Prompt user to bypass reCAPTCHA manually
    print("Please complete the reCAPTCHA in the browser window. Press Enter in the terminal when done.")
    input()  # Wait for user to press Enter

    # Simulate human-like behavior (mouse movement and scrolling)
    ActionChains(driver).move_by_offset(100, 100).perform()
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Save cookies to maintain session
    pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))

    # Wait for page to stabilize
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body")))

    # Check for page reload or redirect
    current_url = driver.current_url
    time.sleep(5)
    if driver.current_url != current_url:
        print("Page reloaded or redirected to:", driver.current_url)
        # Reload cookies and refresh if needed
        driver.delete_all_cookies()
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.refresh()
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body")))

    # Get the rendered HTML
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Initialize data dictionary
    data = {
        "growth score": None,
        "growth last quarter": None,
        "business score": None,
        "headcount": None,
        "news articles": []
    }

    # Extract growth score
    growth_score_elem = soup.select_one("#undefined > section > scores-header > div:nth-child(1) > score-and-trend-big-value > span.score")
    if growth_score_elem:
        data["growth score"] = growth_score_elem.get_text(strip=True)

    # Extract growth last quarter (growth change)
    growth_change_elem = soup.select_one("#undefined > section > scores-header > div:nth-child(1) > score-and-trend-big-value > span.change-label")
    if growth_change_elem:
        data["growth last quarter"] = growth_change_elem.get_text(strip=True)
    else:
        # Fallback to chip-text
        growth_change_fallback = soup.select_one("#undefined > section > scores-header > div:nth-child(1) > score-and-trend-big-value > div.chip-text")
        if growth_change_fallback:
            data["growth last quarter"] = growth_change_fallback.get_text(strip=True)

    # Extract business score (future growth)
    business_score_elem = soup.select_one("#undefined > section > div > div > round-gauge > svg > text")
    if business_score_elem:
        data["business score"] = business_score_elem.get_text(strip=True)

    # Extract headcount
    headcount_elem = soup.select_one("#people > div.section-content > people-highlights > profile-column-layout > tile-highlight:nth-child(1) > mat-card > field-formatter > a")
    if headcount_elem:
        data["headcount"] = headcount_elem.get_text(strip=True)

    # Extract news articles
    news_articles_elems = soup.select("#undefined > section > div:nth-child(1) > div.activity-details > press-reference > div > span:nth-child(2) > a")
    for elem in news_articles_elems:
        text = elem.get_text(strip=True)
        if text:
            data["news articles"].append(text)

    # Convert news articles list to a string
    data["news articles"] = "; ".join(data["news articles"]) if data["news articles"] else None

    # Create Pandas DataFrame
    df = pd.DataFrame([data])
    print(df)

    # Save to CSV
    df.to_csv("scraped_data.csv", index=False)

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    driver.quit()