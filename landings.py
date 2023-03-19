import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

# Read the CSV file
file_path = '/Users/jakewatembach/Desktop/meteoriteLandings/Meteorite_Landings.csv'
df = pd.read_csv(file_path)

# Sort by mass and get the top 15
df = df.sort_values(by='mass (g)', ascending=False).head(15)

# Create a GeoDataFrame
gdf = gpd.GeoDataFrame(
    df, geometry=gpd.points_from_xy(df['reclong'], df['reclat'])
)

# Read world map data
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Plot the world map and meteorite landings
ax = world.boundary.plot(figsize=(15, 10), linewidth=1)
gdf.plot(ax=ax, marker='o', color='red', markersize=50, legend=True)

for x, y, label in zip(gdf.geometry.x, gdf.geometry.y, gdf['name']):
    plt.annotate(label, xy=(x, y), xytext=(3, 3), textcoords='offset points')

plt.title('Top 15 Biggest Meteorite Landings')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()
