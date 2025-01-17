import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# Load data
file_path = 'hamburg_stops.csv'
stops = pd.read_csv(file_path)

columns_to_keep = ['stop_name', 'stop_id', 'stop_lat', 'stop_lon', 'parent_station']
stops = stops[columns_to_keep]

# duplicate stuff
with_parent = stops[stops['parent_station'].notna()]
without_parent = stops[stops['parent_station'].isna()]
with_parent = with_parent.groupby('parent_station', as_index=False).first()
stops = pd.concat([with_parent, without_parent], ignore_index=True)
if 'parent_station' in stops.columns:
    stops = stops.drop(columns=['parent_station'])

#clean busstop names
stops['stop_name'] = stops['stop_name'].str.replace(r'^"|"$', '', regex=True)
stops['stop_name'] = stops['stop_name'].str.replace(',', '', regex=False)
stops['stop_name'] = stops['stop_name'].str.replace(r'\bHamburg,?-?\b', '', regex=True)
stops['stop_name'] = stops['stop_name'].str.strip()

stops = stops[(stops['stop_lat'].between(-90, 90)) & (stops['stop_lon'].between(-180, 180))]

# gml file stuff
districts = gpd.read_file('districts.gml', layer='Bezirke')
districts = districts.to_crs(epsg=4326)
stops['geometry'] = stops.apply(lambda row: Point(row['stop_lon'], row['stop_lat']), axis=1)
stops_gdf = gpd.GeoDataFrame(stops, geometry='geometry', crs="EPSG:4326")
stops_with_districts = gpd.sjoin(stops_gdf, districts, how='left', predicate='within')

if 'Bezirk' in stops_with_districts.columns:
    stops_with_districts['Bezirk'] = stops_with_districts['Bezirk'].astype('Int64')

# more clean
columns_to_keep = ['stop_name', 'stop_lat', 'stop_lon', 'Bezirk', 'Bezirk_Name']
stops_with_districts = stops_with_districts[[col for col in columns_to_keep if col in stops_with_districts.columns]]

# more duplicate drop stuff
stops_with_districts = stops_with_districts.drop_duplicates(subset=['stop_name'], keep='first')

stops_with_districts.to_csv('stops_with_districts.csv', index=False)
print("Stops matched to districts and saved")