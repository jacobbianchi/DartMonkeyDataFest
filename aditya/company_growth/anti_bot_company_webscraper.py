import re
from bs4 import BeautifulSoup

input_file = "/Users/adityacode/DartMonkeyDataFest/aditya/company_growth/input.txt"
output_file = "/Users/adityacode/DartMonkeyDataFest/aditya/company_growth/company.txt"

with open(input_file, "r", encoding="utf-8") as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, "html.parser")

data = {
    "growth score": None,
    "growth last quarter": None,
    "business score": None,
    "headcount": None,
    "news articles": []
}

growth_score_elem = soup.select_one("#undefined > section > scores-header > div:nth-child(1) > score-and-trend-big-value > span.score")
if growth_score_elem:
    data["growth score"] = growth_score_elem.get_text(strip=True)
else:
    growth_score_match = re.search(r'<span class="score">(\d+)</span>', html_content)
    if growth_score_match:
        data["growth score"] = growth_score_match.group(1)

growth_change_elem = soup.select_one("#undefined > section > scores-header > div:nth-child(1) > score-and-trend-big-value > span.change-label")
if growth_change_elem:
    data["growth last quarter"] = growth_change_elem.get_text(strip=True)
else:
    growth_change_fallback = soup.select_one("#undefined > section > scores-header > div:nth-child(1) > score-and-trend-big-value > div.chip-text")
    if growth_change_fallback:
        data["growth last quarter"] = growth_change_fallback.get_text(strip=True)
    else:
        growth_change_match = re.search(r'<span class="change-label">([+-]?\d+%)</span>|<div class="chip-text">([+-]?\d+%)</div>', html_content)
        if growth_change_match:
            data["growth last quarter"] = growth_change_match.group(1) or growth_change_match.group(2)

business_score_elem = soup.select_one("#undefined > section > div > div > round-gauge > svg > text")
if business_score_elem:
    data["business score"] = business_score_elem.get_text(strip=True)
else:
    business_score_match = re.search(r'<text[^>]*>(\d+)/100</text>', html_content)
    if business_score_match:
        data["business score"] = business_score_match.group(1)

headcount_elem = soup.select_one("#people > div.section-content > people-highlights > profile-column-layout > tile-highlight:nth-child(1) > mat-card > field-formatter > a")
if headcount_elem:
    data["headcount"] = headcount_elem.get_text(strip=True)
else:
    headcount_match = re.search(r'<a[^>]*>(\d+)\s*employees?</a>', html_content, re.IGNORECASE)
    if headcount_match:
        data["headcount"] = headcount_match.group(1)

news_articles_elems = soup.select("#undefined > section > div:nth-child(1) > div.activity-details > press-reference > div > span:nth-child(2) > a")
for elem in news_articles_elems:
    text = elem.get_text(strip=True)
    if text:
        data["news articles"].append(text)
else:
    # Regex fallback for news articles
    news_article_matches = re.findall(r'<a[^>]*>([^<]+)</a>\s*(?=<span class="source">)', html_content)
    data["news articles"] = news_article_matches if news_article_matches else []

# Convert news articles list to a semicolon-separated string
data["news articles"] = ";".join(data["news articles"]) if data["news articles"] else ""

# Prepare the line to append (semicolon-separated values)
line = f"{data['growth score'] or ''};{data['growth last quarter'] or ''};{data['business score'] or ''};{data['headcount'] or ''};{data['news articles']}\n"

# Append to company.txt
with open(output_file, "a", encoding="utf-8") as file:
    file.write(line)

print("Data successfully appended to company.txt")