import requests
from duckduckgo_search import DDGS
import urllib.parse
import time
import logging
import os
import random
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# File paths
input_file = "/Users/adityacode/DartMonkeyDataFest/external_data/employee_growth/homeowner_filtered.txt"
output_file = "/Users/adityacode/DartMonkeyDataFest/aditya/employee_growth/search_results.txt"

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# List of user agents for rotation
USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
]

def get_session():
    session = requests.Session()
    retries = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    session.mount("https://", HTTPAdapter(max_retries=retries))
    return session

def duckduckgo_search(name, session):
    try:
        # Initialize DuckDuckGo search
        ddgs = DDGS()
        
        # Construct search query with professional context and location
        query = f"{name} LinkedIn professional profile Dallas Texas"
        logger.info(f"Sending DuckDuckGo search for: {query}")
        
        # Perform search (limit to first 5 results)
        results = []
        for result in ddgs.text(query, max_results=5):
            try:
                title = result.get('title', 'No title')
                link = result.get('href', 'No link')
                description = result.get('body', 'No description')
                
                # Log incomplete results
                if link == 'No link' or title == 'No title':
                    logger.warning(f"Incomplete result for {name}: Title={title}, Link={link}")
                
                results.append({"title": title, "link": link, "description": description})
                
                if len(results) >= 5:
                    break
            except Exception as e:
                logger.warning(f"Error extracting result for {name}: {e}")
                continue
        
        logger.info(f"Retrieved {len(results)} results for {name}")
        return results
    
    except Exception as e:
        logger.error(f"Error during DuckDuckGo search for {name}: {e}")
        return []

def format_search_results(results):
    # Format the search results as a string, using pipes instead of newlines
    formatted = []
    for result in results:
        formatted.append(f"Title: {result['title']}|Link: {result['link']}|Description: {result['description']}")
    return "|".join(formatted) if formatted else "No results found"

def append_to_file(address, name, search_results):
    # Append the result to search_results.txt as a single line
    try:
        with open(output_file, "a", encoding="utf-8") as f:
            # Replace any newlines in search_results with a space
            clean_results = search_results.replace("\n", " ")
            f.write(f"{address};{name};{clean_results};\n")
        logger.info(f"Results for {name} appended to {output_file}")
    except Exception as e:
        logger.error(f"Failed to write to file: {e}")

def main():
    # Verify input file exists
    if not os.path.exists(input_file):
        logger.error(f"Input file {input_file} does not exist")
        return
    
    # Create a session with retry logic
    session = get_session()
    
    try:
        # Read homeowners.txt
        with open(input_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            try:
                address, name = line.split(";")
                name = name[:-3] if name.endswith("&") else name
                logger.info(f"Processing: {name}")
                
                # Perform DuckDuckGo search
                search_results = duckduckgo_search(name, session)
                formatted_results = format_search_results(search_results)
                
                # Append to file
                append_to_file(address, name, formatted_results)
                
                # Random delay to avoid overwhelming the server
                time.sleep(random.uniform(1.5, 3))
            
            except ValueError as e:
                logger.warning(f"Invalid line format: {line} - {e}")
                continue
    
    except Exception as e:
        logger.error(f"An error occurred in main: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    main()