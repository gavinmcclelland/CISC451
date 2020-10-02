import pandas as pd

df = pd.read_csv("datasets\\point-of-interest.csv", ';')
downtown_point = df.loc[df['NAME'] == 'DOWNTOWN TRANSFER POINT', 'geo_point_2d'].values[0]
print(downtown_point)
downtown_lon = float(downtown_point.split(',')[0])
downtown_lat = float(downtown_point.split(',')[1])

df = pd.read_csv("datasets\\driveways.csv", ';')
driveway_coords = df['geo_point_2d'].str.split(',', expand=True).astype(float).rename(columns={0:'Latitude', 1:'Longitude'})
driveway_coords_tuples = zip(driveway_coords['Latitude'], driveway_coords['Longitude'])
for p in driveway_coords_tuples:
    print(p)