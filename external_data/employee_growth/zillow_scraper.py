from bs4 import BeautifulSoup
import re

def extract_addresses(html_content):
    # Create BeautifulSoup object to parse HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find all address tags
    address_tags = soup.find_all('address')
    
    # Extract text content from each address tag
    addresses = [tag.get_text(strip=True) for tag in address_tags]
    
    # Clean up addresses (remove extra whitespace and newlines)
    addresses = [re.sub(r'\s+', ' ', addr) for addr in addresses]
    
    # Write addresses to file, separated by commas
    with open('/Users/adityacode/DartMonkeyDataFest/aditya/employee_growth/addresses.txt', 'w', encoding='utf-8') as f:
        f.write(';\n'.join(addresses))

# Example usage
if __name__ == "__main__":
    # Sample HTML content (can be replaced with file input or URL fetch)
    with open("/Users/adityacode/DartMonkeyDataFest/aditya/employee_growth/input.txt", "r", encoding="utf-8") as file:
        sample_html = file.read()
    
    extract_addresses(sample_html)