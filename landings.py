import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx
from adjustText import adjust_text
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

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

fig, ax = plt.subplots(figsize=(20, 10))
ax.set_aspect('equal')  
ax.margins(x=0.05)

world.plot(ax=ax, edgecolor='white', linewidth=0.5, facecolor='green', alpha=0.3)
ctx.add_basemap(ax, source=ctx.providers.CartoDB.Positron)



meteorite_img = plt.imread('/Users/jakewatembach/Desktop/meteoriteLandings/meteorite.png')

# Get the dimensions of the meteorite image
img_height, img_width, _ = meteorite_img.shape

# Calculate the offset between the center of the meteorite and the center of the flame behind it
x_offset = int(img_width * 0.26)
y_offset = int(img_height * 0.27)

for x, y in zip(gdf.geometry.x, gdf.geometry.y):
    imagebox = OffsetImage(meteorite_img, zoom=0.03)
    ab = AnnotationBbox(imagebox, (x - x_offset, y - y_offset), frameon=False, box_alignment=(0.5, 0.5))
    ax.add_artist(ab)


texts = []
bbox = ax.get_xlim() + ax.get_ylim()

# Calculate the range of the meteorite locations in x and y directions
meteorites_bbox = gdf.total_bounds
x_range = meteorites_bbox[2] - meteorites_bbox[0]
y_range = meteorites_bbox[3] - meteorites_bbox[1]



# Adjust the label positions to ensure they're within the bounds of the plot
for x, y, name, mass in zip(gdf.geometry.x, gdf.geometry.y, gdf['name'], gdf['mass (t)']):
    label = f"{name} ({mass:.2f} t)"

    # Calculate the offset of the label from the meteorite
    label_offset = (0.03 * x_range, 0.03 * y_range)
    if x < bbox[0]:
        label_offset = (-0.03 * x_range, label_offset[1])
    elif x > bbox[1]:
        label_offset = (0.03 * x_range, label_offset[1])
    if y < bbox[2]:
        label_offset = (label_offset[0], -0.03 * y_range)
    elif y > bbox[3]:
        label_offset = (label_offset[0], 0.03 * y_range)

    # Adjust the label position based on the offset
    label_x = x + label_offset[0]
    label_y = y + label_offset[1]

    # Adjust the label position so that it is within the bounds of the plot
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
padding_factor = 0.2

x_range = meteorites_bbox[2] - meteorites_bbox[0]
y_range = meteorites_bbox[3] - meteorites_bbox[1]

ax.set_xlim(meteorites_bbox[0] - x_range * padding_factor, meteorites_bbox[2] + x_range * padding_factor)
ax.set_ylim(meteorites_bbox[1] - y_range * padding_factor, meteorites_bbox[3] + y_range * padding_factor)

plt.xticks(fontsize=8)
plt.yticks(fontsize=8)

plt.title('Top 10 Biggest Meteorite Landings', fontsize=20, color='white')

plt.savefig('meteorite_landings.png', dpi=300, bbox_inches='tight')
plt.show()
