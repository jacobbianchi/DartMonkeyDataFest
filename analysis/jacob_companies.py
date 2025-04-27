import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Setup
nltk.download('vader_lexicon')
sns.set_theme(style="whitegrid")  # Prettier graphs

# 1. Load the scores dataset (your company.txt)
file_path = '/Users/jacobbia/Documents/UCLA/DartMonkeyDataFest/external_data/company.txt'
with open(file_path, 'r', encoding='utf-8') as f:
    raw_data = f.readlines()

companies = []
for line in raw_data:
    parts = line.strip().split(';')
    if len(parts) >= 8:
        companies.append({
            'Company': parts[0],
            'Growth_Score': parts[1].replace('pts', '').strip(),
            'Growth_Change_Q': parts[2].replace('pts', '').strip(),
            'Heat_Score': parts[3].replace('pts', '').strip(),
            'Heat_Change': parts[4].replace('pts', '').strip(),
            'Business_Score': parts[5].strip(),
            'Headcount': parts[6],
            'News': parts[7]
        })

df_scores = pd.DataFrame(companies)

for col in ['Growth_Score', 'Growth_Change_Q', 'Heat_Score', 'Heat_Change', 'Business_Score']:
    df_scores[col] = pd.to_numeric(df_scores[col], errors='coerce')

def parse_headcount(value):
    if '-' in value:
        low, high = map(float, value.split('-'))
        return (low + high) / 2
    elif '+' in value:
        base = float(value.replace('+', ''))
        return base + np.random.uniform(0, 5000)  # add random 0-5000
    else:
        try:
            return float(value)
        except:
            return np.nan

# Apply the function
df_scores['Headcount'] = df_scores['Headcount'].apply(parse_headcount)

# NLP Sentiment analysis
sia = SentimentIntensityAnalyzer()

def calculate_sentiment(news_text):
    if not news_text or pd.isna(news_text):
        return 0
    headlines = [h.strip() for h in news_text.split('~') if h.strip()]
    sentiments = [sia.polarity_scores(headline)['compound'] for headline in headlines]
    return sum(sentiments) / len(sentiments) if sentiments else 0

df_scores['News_Sentiment'] = df_scores['News'].apply(calculate_sentiment)
df_scores['News_Count'] = df_scores['News'].apply(lambda x: len(x.split('~')) if isinstance(x, str) else 0)

# 2. Load your market dataset
market_file_path = '/Users/jacobbia/Documents/UCLA/DartMonkeyDataFest/data/Leases.csv'  # replace with the actual path
df_market = pd.read_csv(market_file_path)

# 3. Merge on Company name
df_merged = pd.merge(
    df_scores,
    df_market[['company_name', 'market']],
    how='left',
    left_on='Company',
    right_on='company_name'
)

# 4. Clean up merged DataFrame
df_merged.drop('company_name', axis=1, inplace=True)

# After merging df_scores and df_market into df_merged...

# 1. Standardize 'market' values (make lower case to match easily)
df_merged['market'] = df_merged['market'].str.lower()

# 2. Define target markets
target_markets = ['san francisco', 'manhattan', 'dallas/ft worth']

# 3. Filter for only those markets
df_merged = df_merged[df_merged['market'].isin(target_markets)]

# (Optional) Capitalize market names again for prettier labels
df_merged['market'] = df_merged['market'].str.title()

# ✅ Now all plots will only show SF, NY, Dallas companies

custom_palette = {
   "Dallas/Ft Worth": "#654321",          # dark brown
   "Manhattan": "#e07b91",        # soft pink-red
   "San Francisco": "#88b04b"    # soft green
}

# -------------------------
# PLOT 4: Sentiment vs Growth Score Change
plt.figure(figsize=(12,6))
sns.scatterplot(data=df_merged, x='Headcount', y='Growth_Change_Q', hue='market', s=300, palette=custom_palette, alpha=0.9)
plt.title('Headcount vs Growth Score Change (SF, NY, Dallas)', fontsize=16)
plt.xlabel('Headcount')
plt.ylabel('Growth Score Change')
plt.axhline(0, color='grey', linestyle='--')
plt.grid(True)
plt.show()