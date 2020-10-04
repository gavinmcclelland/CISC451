import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go

import flask
import pandas as pd
import time
import os
import json

# Create webserver
server = flask.Flask('app')
server.secret_key = os.environ.get('secret_key', 'secret')

# Load transit data and remove data with non-functioning GPS coordinates
transit_data = pd.read_csv("datasets\\Transit Data - October.csv")
print(transit_data.shape)
transit_data = transit_data[transit_data.Latitude > 44]
print(transit_data.shape)
transit_data = transit_data[transit_data.Longitude < -76]
print(transit_data.shape)
# Groupby COordinates to reduce number of discete points
clean = transit_data.groupby(['Latitude', 'Longitude']).size().reset_index(name='counts')
print(clean.head())
print(clean.shape)



# Load geojson files for the background layers
with open("A1_geo\\neighbourhoods.geojson", "r") as geo:
    neighbourhood_geojson = json.load(geo)
with open("A1_geo\\transit-gtfs-routes.geojson", "r") as geo:
    routes_geojson = json.load(geo)
# Create list of colors to use when generating neighbourhood layers
colors = [
    "firebrick",
    "floralwhite",
    "forestgreen",
    "fuchsia",
    "gainsboro",
    "ghostwhite",
    "gold",
    "goldenrod",
    "gray",
    "grey",
    "green",
    "greenyellow",
    "honeydew",
    "hotpink",
    "indianred",
    "indigo",
    "ivory",
    "khaki",
    "lavender",
    "lavenderblush",
    "lawngreen",
    "lemonchiffon",
    "lightblue",
    "lightcoral",
    "lightcyan",
    "lightgoldenrodyellow",
    "lightgray",
    "lightgrey",
    "lightgreen",
    "lightpink",
    "lightsalmon",
    "lightseagreen",
    "lightskyblue",
    "lightslategray",
    "lightslategrey",
    "lightsteelblue",
    "lightyellow",
    "lime",
    "limegreen",
    "linen",
    "magenta",
    "maroon",
    "mediumaquamarine",
    "mediumblue",
    "mediumorchid",
    "mediumpurple",
    "mediumseagreen",
    "mediumslateblue",
    "mediumspringgreen",
    "mediumturquoise",
    "mediumvioletred",
    "midnightblue",
    "mintcream",
    "mistyrose",
    "moccasin",
    "navajowhite",
    "navy",
    "oldlace",
    "olive",
    "olivedrab",
    "orange",
    "orangered"
]

layers = []
# Create a list of features for each neighbourhood (to color each individually)
for n, neighbourhood in enumerate(neighbourhood_geojson['features']):
    layers.append(
        {
            'visible': True,
            'source': neighbourhood,
            'type': "fill",
            'below': "traces",
            'color': colors[n],
            'opacity': 0.6
        }
    )
# Add the transit routes geojson to the layers list
layers.append(
    {
        'visible': True,
        'source': routes_geojson,
        'type': "line",
        'below': "traces",
        'color': "orangered",
        'opacity': 1
    }
)
# Create a plotly Densitymapbox plot for the transit locations
fig = go.Figure(go.Densitymapbox(
    lon = clean.Longitude,
    lat = clean.Latitude,
    z=clean.counts,
    radius=15
    ))
# Specify stylistic preferences and add in background layers (neighbourhoods and transit routes)
fig.update_layout(
    height=700,
    mapbox = {
        'style': "stamen-terrain",
        'center': {"lat": 44.227860, "lon": -76.496938},
        'zoom': 10,
        'layers': layers
            },
    margin = {'l':0, 'r':0, 'b':0, 't':0})
# Use more efficient rendering widget
f = go.FigureWidget(fig)
# Create dash app
app = dash.Dash('app', server=server)
app.scripts.config.serve_locally = False
dcc._js_dist[0]['external_url'] = 'https://cdn.plot.ly/plotly-basic-latest.min.js'
# Create the basic layout of the dash app
app.layout = html.Div([
    html.H1('Transit Data Heatmap'),
    dcc.Graph(id='my-graph', figure=f)
], className="container")

# Run dash app
if __name__ == '__main__':
    app.run_server()


