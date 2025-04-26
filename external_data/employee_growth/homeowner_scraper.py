from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import re
import time
import os

# Path to your text file with semicolon-separated addresses
ADDRESS_FILE = "/Users/adityacode/DartMonkeyDataFest/aditya/employee_growth/addresses.txt"
OUTPUT_FILE = "/Users/adityacode/DartMonkeyDataFest/aditya/employee_growth/homeowner.txt"

# Initialize Selenium WebDriver (assuming Chrome)
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode
driver = webdriver.Chrome(options=options)

def parse_address(address):
    # Split by comma to get street part
    parts = address.split(",")
    street_part = parts[0].strip()
    
    # Split street part into words
    words = street_part.split()
    if not words:
        return None, None, None
    
    # Extract street number (first word, if it's a number)
    street_number = words[0] if words[0].isdigit() else None
    
    # Check for direction (N, S, E, W) as second word
    direction = None
    street_name_words = words[1:] if words[0].isdigit() else words
    if street_name_words and street_name_words[0] in ["N", "S", "E", "W"]:
        direction = street_name_words[0]
        street_name_words = street_name_words[1:]
    
    # Ignore the last word (street type like St, Ave, etc.)
    if street_name_words:
        street_name_words = street_name_words[:-1]
    
    # Join remaining words for street name
    street_name = " ".join(street_name_words) if street_name_words else None
    
    return street_number, direction, street_name

def extract_results(street_number, street_name):
    while True:
        try:
            # Wait for results table to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "SearchResults1_dgResults"))
            )
            
            # Find all rows in the results table
            rows = driver.find_elements(By.XPATH, "//table[@id='SearchResults1_dgResults']/tbody/tr")
            for row in rows:
                # Skip header and pagination rows
                if "matches" in row.text or "Property Address" in row.text:
                    continue
                
                # Extract columns
                cols = row.find_elements(By.TAG_NAME, "td")
                if len(cols) >= 4:  # Ensure row has enough columns
                    address = cols[1].text.strip()
                    owner_name = cols[3].text.strip().replace("\n", " ")  # Handle multi-line owner names
                    
                    # Check if street name and number match (case-insensitive)
                    if (street_name.lower() in address.lower() and 
                        address.lower().startswith(street_number.lower())):
                        return f"{address};{owner_name}"
            
            # Check for "NEXT >" link
            try:
                next_link = driver.find_element(By.LINK_TEXT, "NEXT >")
                next_link.click()
                time.sleep(1)  # Wait for page to load
            except:
                return None  # No more pages
        except Exception as e:
            print(f"Error extracting results: {str(e)}")
            return None

def search_address(street_number, direction, street_name):
    try:
        # Navigate to the search page
        driver.get("https://www.dallascad.org/SearchAddr.aspx")
        
        # Wait for the page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "txtStName"))
        )
        
        # Input street name
        street_name_field = driver.find_element(By.ID, "txtStName")
        street_name_field.clear()
        street_name_field.send_keys(street_name)
        
        # Set direction if present
        if direction:
            direction_dropdown = Select(driver.find_element(By.ID, "listStDir"))
            direction_dropdown.select_by_value(direction)
        
        # Select Dallas from city dropdown
        city_dropdown = Select(driver.find_element(By.ID, "listCity"))
        city_dropdown.select_by_visible_text("DALLAS")
        
        # Submit the search
        submit_button = driver.find_element(By.ID, "cmdSubmit")
        submit_button.click()
        
        # Wait for results page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "SearchResults1_dgResults"))
        )
        
        # Extract results (return first match only)
        result = extract_results(street_number, street_name)
        return result
    except Exception as e:
        print(f"Error processing {street_name}: {str(e)}")
        return None

def append_to_file(result):
    # Append result to output file
    with open(OUTPUT_FILE, "a") as file:
        file.write(result + "\n")

def main():
    # Clear output file if it exists
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)
        
    try:
        # Read addresses from file
        with open(ADDRESS_FILE, "r") as file:
            addresses = file.read().split(";")
        
        for address in addresses:
            address = address.strip()
            if not address:
                continue
                
            street_number, direction, street_name = parse_address(address)
            if street_name and street_number:
                print(f"Processing: {street_number} {direction or ''} {street_name}")
                result = search_address(street_number, direction, street_name)
                if result:
                    append_to_file(result)
                    print(f"Found match for {street_number} {direction or ''} {street_name}")
                else:
                    print(f"No match for {street_number} {direction or ''} {street_name}")
                time.sleep(0.5)  # Reduced wait time
            else:
                print(f"Failed to parse address: {address}")
                
        print(f"Results saved to {OUTPUT_FILE}")
                
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()