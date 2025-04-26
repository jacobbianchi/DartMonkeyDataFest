import re
from bs4 import BeautifulSoup
from lxml import etree

input_file = "/Users/anthonychen/Desktop/Year3/DF2025/DartMonkeyDataFest/external_data/company_growth/input.txt"
output_file = "/Users/anthonychen/Desktop/Year3/DF2025/DartMonkeyDataFest/external_data/company_growth/company.txt"

with open(input_file, "r", encoding="utf-8") as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, "html.parser")
parser = etree.HTMLParser()
tree = etree.fromstring(html_content, parser)

data = {
    "company name": None,
    "growth score": None,
    "growth last quarter": None,
    "heat score": None,
    "heat score change": None,
    "business score": None,
    "headcount": None,
    "news articles": []
}

#company name
company_name_elem = soup.select_one("body > chrome > div > mat-sidenav-container > mat-sidenav-content > div > profile > page-layout > div.header > profile-v3-header > div > div.content > div.top-row > div.top-row-left.ng-star-inserted > span.entity-name.ng-star-inserted")
if company_name_elem:
    data["company name"] = company_name_elem.get_text(strip=True)
else:
    company_name_match = re.search(r'<span class="entity-name">([^<]+)</span>', html_content)
    if company_name_match:
        data["company name"] = company_name_match.group(1)

# Growth score
growth_score_elem = soup.select_one("#undefined > section > scores-header > div:nth-child(1) > score-and-trend-big-value > span.score")
if growth_score_elem:
    data["growth score"] = growth_score_elem.get_text(strip=True)
else:
    growth_score_match = re.search(r'<span class="score">(\d+)</span>', html_content)
    if growth_score_match:
        data["growth score"] = growth_score_match.group(1)

# Growth score change (corrected selector)
growth_change_elem = soup.select_one("#undefined > section > scores-header > div:nth-child(1) > score-and-trend-big-value > square-chip > div > div")
if growth_change_elem:
    data["growth last quarter"] = growth_change_elem.get_text(strip=True)
else:
    growth_change_match = re.search(r'<div class="chip-text">([+-]?\d+%)</div>', html_content)
    if growth_change_match:
        data["growth last quarter"] = growth_change_match.group(1)

# Heat score
heat_score_elem = soup.select_one("#undefined > section > scores-header > div:nth-child(2) > score-and-trend-big-value > span.score")
if heat_score_elem:
    data["heat score"] = heat_score_elem.get_text(strip=True)
else:
    heat_score_match = re.search(r'<span class="score">(\d+)</span>', html_content)
    if heat_score_match:
        data["heat score"] = heat_score_match.group(1)

# Heat score change
heat_change_elem = soup.select_one("#undefined > section > scores-header > div:nth-child(2) > score-and-trend-big-value > square-chip > div > div")
if heat_change_elem:
    data["heat score change"] = heat_change_elem.get_text(strip=True)
else:
    heat_change_match = re.search(r'<div class="chip-text">([+-]?\d+%)</div>', html_content)
    if heat_change_match:
        data["heat score change"] = heat_change_match.group(1)

# Business score
business_score_elem = soup.select_one("#undefined > section > div > div > round-gauge > svg > text")
if business_score_elem:
    data["business score"] = business_score_elem.get_text(strip=True)
else:
    business_score_match = re.search(r'<text[^>]*>(\d+)/100</text>', html_content)
    if business_score_match:
        data["business score"] = business_score_match.group(1)

# Headcount
headcount_elem = soup.select_one("#people > div.section-content > people-highlights > profile-column-layout > tile-highlight:nth-child(1) > mat-card > field-formatter > a")
if headcount_elem:
    data["headcount"] = headcount_elem.get_text(strip=True)
else:
    headcount_match = re.search(r'<a[^>]*>(\d+)\s*employees?</a>', html_content, re.IGNORECASE)
    if headcount_match:
        data["headcount"] = headcount_match.group(1)

xpaths = [
    '//*[@id="undefined"]/section/div[1]/div[2]/press-reference/div',
    '//*[@id="undefined"]/section/div[2]/div[2]/press-reference/div',
    '//*[@id="undefined"]/section/div[3]/div[2]/press-reference/div',
    '//*[@id="undefined"]/section/div[4]/div[2]/press-reference/div'
]
title_set = set()
for xpath in xpaths:
    elements = tree.xpath(xpath)
    for elem in elements:
        title = elem.get('title')
        if title:
            title_set.add(title.strip())
if title_set:
    data["news articles"] = list(title_set)


# Fallback for news articles if none found
if not data["news articles"]:
    news_article_matches = re.findall(r'<a[^>]*>([^<]+)</a>\s*(?=<span class="source">)', html_content)
    data["news articles"] = news_article_matches if news_article_matches else []

# Convert news articles list to a ~-separated string
data["news articles"] = " ~ ".join(data["news articles"]) if data["news articles"] else ""

# Prepare the line to append (semicolon-separated values)
line = f"{data['company name']};{data['growth score'] or ''};{data['growth last quarter'] or ''};{data['heat score'] or ''};{data['heat score change'] or ''};{data['business score'] or ''};{data['headcount'] or ''};{data['news articles']}\n"

# Append to company.txt
with open(output_file, "a", encoding="utf-8") as file:
    file.write(line)

print("Data successfully appended to company.txt")