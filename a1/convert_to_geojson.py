import json
import pandas as pd

transit_data = pd.read_csv("datasets\\Transit Data - October.csv", ',')
print(transit_data.shape)
transit_data = transit_data[transit_data.Latitude > 44]
print(transit_data.shape)
transit_data = transit_data[transit_data.Longitude < -76]
print(transit_data.shape)
transit_list = [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [lon, lat]}, "properties": {"Date": date, "Time": time}, "id": ID} for lon, lat, date, time, ID in zip(transit_data.Longitude, transit_data.Latitude, transit_data.Date, transit_data.Time, transit_data.index)]
transit_geojson = {"type": "FeatureCollection", "features": transit_list}
with open('datasets\\transit_data.geojson', 'w') as out:
    json.dump(transit_geojson, out)
