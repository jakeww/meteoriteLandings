import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx
from adjustText import adjust_text

# Read the CSV file
file_path = '/Users/jakewatembach/Desktop/meteoriteLandings/Meteorite_Landings.csv'
df = pd.read_csv(file_path)

df['mass (t)'] = df['mass (g)'] / 1e6

df = df.sort_values(by='mass (t)', ascending=False).head(10)

gdf = gpd.GeoDataFrame(
    df, geometry=gpd.points_from_xy(df['reclong'], df['reclat'])
)

gdf.crs = 'EPSG:4326'
gdf = gdf.to_crs('EPSG:3857')

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
world = world.to_crs('EPSG:3857')

plt.style.use('dark_background')
plt.rcParams['font.family'] = 'Arial'

fig, ax = plt.subplots(figsize=(15, 10))
world.plot(ax=ax, edgecolor='white', linewidth=0.5, color='whitesmoke', alpha=0.3)
gdf.plot(ax=ax, marker='o', color='lime', edgecolor='black', markersize=100, legend=True, zorder=3)

ctx.add_basemap(ax, source=ctx.providers.Stamen.TonerLite)

texts = []
bbox = ax.get_xlim() + ax.get_ylim()
for x, y, name, mass in zip(gdf.geometry.x, gdf.geometry.y, gdf['name'], gdf['mass (t)']):
    label = f"{name} ({mass:.2f} t)"
    label_x = x + (x * 0.01)
    label_y = y + (y * 0.01)
    if label_x < bbox[0]:
        label_x = bbox[0] + (bbox[1] - bbox[0]) * 0.01
    if label_x > bbox[1]:
        label_x = bbox[1] - (bbox[1] - bbox[0]) * 0.01
    if label_y < bbox[2]:
        label_y = bbox[2] + (bbox[3] - bbox[2]) * 0.01
    if label_y > bbox[3]:
        label_y = bbox[3] - (bbox[3] - bbox[2]) * 0.01
    texts.append(ax.text(label_x, label_y, label, fontsize=10, ha='center', va='center', color='white',
                bbox=dict(boxstyle="round", fc="black", alpha=0.5)))
adjust_text(texts)

ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')

meteorites_bbox = gdf.total_bounds
padding_factor = 0.1

x_range = meteorites_bbox[2] - meteorites_bbox[0]
y_range = meteorites_bbox[3] - meteorites_bbox[1]

ax.set_xlim(meteorites_bbox[0] - x_range * padding_factor, meteorites_bbox[2] + x_range * padding_factor)
ax.set_ylim(meteorites_bbox[1] - y_range * padding_factor, meteorites_bbox[3] + y_range * padding_factor)

plt.xticks(fontsize=8)
plt.yticks(fontsize=8)

plt.title('Top 10 Biggest Meteorite Landings', fontsize=20, color='white')

plt.savefig('meteorite_landings.png', dpi=300, bbox_inches='tight')
plt.show()
