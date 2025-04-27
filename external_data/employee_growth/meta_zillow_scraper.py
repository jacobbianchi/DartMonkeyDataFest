from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape_zillow():
    # Set up Chrome options
    chrome_options = Options()
    # Comment out headless mode to mimic real browser
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    # Initialize WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    output_file = "/Users/adityacode/DartMonkeyDataFest/external_data/employee_growth/input.txt"
    page_index = 1
    max_retries = 3
    
    try:
        while True:
            # Construct URL
            url = f"https://www.zillow.com/dallas-tx/sold/{page_index}_p/"
            print(f"Scraping page {page_index}: {url}")
            
            retries = 0
            while retries < max_retries:
                try:
                    # Navigate to page
                    driver.get(url)
                    
                    # Wait for the target element to be visible (up to 20 seconds)
                    try:
                        grid = WebDriverWait(driver, 20).until(
                            EC.visibility_of_element_located((By.CSS_SELECTOR, "ul.photo-cards"))
                        )
                    except TimeoutException:
                        print(f"Timeout: Could not find ul.photo-cards on page {page_index}, retry {retries + 1}/{max_retries}")
                        retries += 1
                        time.sleep(2)  # Wait before retrying
                        continue
                    
                    # Get all li children
                    list_items = grid.find_elements(By.TAG_NAME, "li")
                    
                    if not list_items:
                        print("No more listings found. Stopping.")
                        return
                    
                    # Get HTML content of the entire ul element
                    grid_html = grid.get_attribute("outerHTML")
                    
                    # Append to file
                    with open(output_file, "a", encoding="utf-8") as f:
                        f.write(f"\n\n--- Page {page_index} ---\n")
                        f.write(grid_html)
                    
                    page_index += 1
                    break  # Exit retry loop on success
                
                except Exception as e:
                    print(f"Error on page {page_index}, retry {retries + 1}/{max_retries}: {str(e)}")
                    retries += 1
                    time.sleep(2)
                    if retries == max_retries:
                        print(f"Max retries reached for page {page_index}. Stopping.")
                        return
                
    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_zillow()