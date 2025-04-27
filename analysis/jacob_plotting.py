import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

df_merged = pd.read_csv('merged_data.csv')

custom_palette = {
   "Dallas/Ft Worth": "#654321",          # dark brown
   "Manhattan": "#e07b91",        # soft pink-red
   "San Francisco": "#88b04b"    # soft green
}

# -------------------------
# PLOT 4: Sentiment vs Growth Score Change
plt.figure(figsize=(12,6))
sns.scatterplot(data=df_merged, x='Headcount', y='Growth_Change_Q', hue='market', s=300, palette=custom_palette, alpha=0.9)
plt.title('Company Size vs Growth Score', fontsize=16)
plt.xlabel('Headcount')
plt.ylabel('Growth Score')
plt.axhline(0, color='grey')
plt.grid(True)

# Add mean Growth_Change_Q lines for each market
for market in df_merged['market'].unique():
    mean_growth = df_merged[df_merged['market'] == market]['Growth_Change_Q'].mean()
    color = custom_palette[market]  # Match the hue color
    plt.axhline(mean_growth, color=color, linestyle='--', linewidth=2, label=f'{market} Avg')

plt.legend()
plt.show()