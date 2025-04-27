import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Load data
df_merged = pd.read_csv('merged_data.csv')

# Color palette
custom_palette = {
    "Dallas/Ft Worth": "#654321",    # dark brown
    "Manhattan": "#e07b91",          # soft pink-red
    "San Francisco": "#88b04b"       # soft green
}

# Set style
sns.set_theme(style="white", rc={
    "axes.edgecolor": "black",
    "axes.linewidth": 4.0,
    "grid.color": "0.85",
    "axes.facecolor": "#fcf4e8",
    "figure.facecolor": "#fcf4e8"
})

# Create plot
fig, ax = plt.subplots(figsize=(12, 8))

# Scatterplot
sns.scatterplot(
    data=df_merged,
    x='Headcount',
    y='Growth_Change_Q',
    hue='market',
    palette=custom_palette,
    s=300,
    alpha=0.9,
    edgecolor='black',     # Add black edge around points for pop
    linewidth=1.2,
    ax=ax
)

# Title and labels
ax.set_title("Company Size vs Growth Score", fontsize=24, fontweight='bold', pad=20)
ax.set_xlabel("Headcount", fontsize=20)
ax.set_ylabel("Growth Score Change", fontsize=20)

# Axis ticks
ax.tick_params(axis='x', labelsize=14)
ax.tick_params(axis='y', labelsize=14)

# Horizontal baseline at Growth Change = 0
ax.axhline(0, color='grey', linestyle='--', linewidth=2)

# Mean Growth_Change_Q lines per market
for market in df_merged['market'].unique():
    mean_growth = df_merged[df_merged['market'] == market]['Growth_Change_Q'].mean()
    color = custom_palette[market]
    ax.axhline(mean_growth, color=color, linestyle='--', linewidth=3, label=f'{market} Avg')

# Legend
ax.legend(title='', fontsize=16, loc='lower center', bbox_to_anchor=(0.5, -0.3), ncol=3)

# Grid
ax.grid(True, which='major', axis='y', linestyle='--', alpha=0.5)

# Remove top and right spines
sns.despine()

# Tight layout
plt.tight_layout(pad=2)

# Save as transparent
plt.savefig("company_size_vs_growth_score.png", dpi=300, bbox_inches='tight', transparent=True)

# Show plot
plt.show()