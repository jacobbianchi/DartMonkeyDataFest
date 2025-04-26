import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx

# --- Load the geocoded CSV ---
df = pd.read_csv('jacob/geocoded_addresses.csv')

# --- Build GeoDataFrame ---
gdf = gpd.GeoDataFrame(
    df,
    geometry=gpd.points_from_xy(df.longitude, df.latitude),
    crs='EPSG:4326'
)

# Reproject for basemap
gdf = gdf.to_crs(epsg=3857)

# --- Color map ---
industry_colors = {
    'Healthcare': 'red',
    'Education': 'blue',
    'Technology': 'green',
    'Legal Services': 'purple',
    'Finance': 'orange',
    'Government': 'brown',
    'Manufacturing': 'pink'
}

# --- Plot ---
fig, ax = plt.subplots(figsize=(12, 12))

for industry, color in industry_colors.items():
    subset = gdf[gdf['predicted_industry'] == industry]
    subset.plot(ax=ax, markersize=60, color=color, label=industry, alpha=0.8, marker='o', edgecolor='black')

ctx.add_basemap(ax, source=ctx.providers.CartoDB.Positron)

ax.set_axis_off()
ax.legend(title="Predicted Industry", loc='lower left')
plt.title('Houses Color-Coded by Predicted Industry', fontsize=16)

# --- Save or Show ---
plt.savefig('jacob/houses_map_by_industry.png', dpi=300, bbox_inches='tight')
plt.show()

print("✅ Map created and saved as 'jacob/houses_map_by_industry.png'.")