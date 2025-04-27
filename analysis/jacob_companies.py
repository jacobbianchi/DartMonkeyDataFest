import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Setup
nltk.download('vader_lexicon')
sns.set_theme(style="whitegrid")  # Prettier graphs

# 1. Load the data
file_path = '/Users/jacobbia/Documents/UCLA/DartMonkeyDataFest/external_data/company.txt'
with open(file_path, 'r', encoding='utf-8') as f:
    raw_data = f.readlines()

# 2. Parse data correctly
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

# Create DataFrame
df = pd.DataFrame(companies)

# Convert numeric fields
for col in ['Growth_Score', 'Growth_Change_Q', 'Heat_Score', 'Heat_Change', 'Business_Score']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Extract headcount lower bound
df['Headcount_Lower'] = df['Headcount'].str.extract(r'(\d+)').astype(float)

# Proper NLP on each news article separately
sia = SentimentIntensityAnalyzer()

def calculate_sentiment(news_text):
    if not news_text or pd.isna(news_text):
        return 0
    headlines = [h.strip() for h in news_text.split('~') if h.strip()]
    sentiments = []
    for headline in headlines:
        score = sia.polarity_scores(headline)['compound']
        sentiments.append(score)
    if sentiments:
        return sum(sentiments) / len(sentiments)
    else:
        return 0

df['News_Sentiment'] = df['News'].apply(calculate_sentiment)

# Number of News Articles
df['News_Count'] = df['News'].apply(lambda x: len(x.split('~')) if isinstance(x, str) else 0)

# -------------------------
# PLOT 1: Distribution of Growth Score Changes
plt.figure(figsize=(10,6))
sns.histplot(df['Growth_Change_Q'].dropna(), bins=30, kde=True, color="dodgerblue")
plt.title('Distribution of Growth Score Changes', fontsize=16)
plt.xlabel('Growth Score Change (Last Quarter)', fontsize=12)
plt.ylabel('Number of Companies')
plt.grid(True)
plt.show()

# -------------------------
# PLOT 2: Heat Change vs Business Score
plt.figure(figsize=(12,6))
sns.scatterplot(data=df, x='Heat_Change', y='Business_Score', hue='Growth_Change_Q', palette='coolwarm', size='Growth_Score', sizes=(40, 400))
plt.title('Heat Change vs Business Score (colored by Growth)', fontsize=16)
plt.xlabel('Heat Score Change', fontsize=12)
plt.ylabel('Business Score', fontsize=12)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.show()

# -------------------------
# PLOT 3: Company Size vs Growth Score
plt.figure(figsize=(12,6))
sns.violinplot(data=df, x='Headcount_Lower', y='Growth_Score', palette='muted', inner="quartile")
plt.title('Growth Score by Company Size (Lower Bound)', fontsize=16)
plt.xlabel('Headcount Lower Bound', fontsize=12)
plt.ylabel('Growth Score', fontsize=12)
plt.grid(True)
plt.show()

# -------------------------
# PLOT 4: News Sentiment vs Growth and Heat
plt.figure(figsize=(12,6))
sns.scatterplot(data=df, x='News_Sentiment', y='Growth_Change_Q', size='News_Count', sizes=(20, 300), hue='Heat_Change', palette='vlag')
plt.title('News Sentiment vs Growth Score Change (Size = # of Articles)', fontsize=16)
plt.xlabel('Average News Sentiment', fontsize=12)
plt.ylabel('Growth Score Change', fontsize=12)
plt.axhline(0, color='grey', linestyle='--')
plt.grid(True)
plt.show()

# -------------------------
# PLOT 5: Top Movers
top_movers = df[['Company', 'Growth_Change_Q']].dropna()
top_movers['abs_change'] = top_movers['Growth_Change_Q'].abs()
top_movers = top_movers.sort_values('abs_change', ascending=False).head(15)

plt.figure(figsize=(12,8))
sns.barplot(data=top_movers, y='Company', x='Growth_Change_Q', palette="Spectral")
plt.title('Top 15 Companies by Growth Score Movement', fontsize=16)
plt.xlabel('Growth Score Change', fontsize=12)
plt.ylabel('Company')
plt.axvline(0, color='black', linestyle='--')
plt.grid(True)
plt.show()
