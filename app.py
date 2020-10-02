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

server = flask.Flask('app')
server.secret_key = os.environ.get('secret_key', 'secret')


transit_data = pd.read_csv("datasets\\Transit Data - October.csv")
print(transit_data.shape)
transit_data = transit_data[transit_data.Latitude > 44]
print(transit_data.shape)
transit_data = transit_data[transit_data.Longitude < -76]
print(transit_data.shape)
clean = transit_data.groupby(['Latitude', 'Longitude']).size().reset_index(name='counts')
print(clean.head())
print(clean.shape)




# with open("A1_geo\\neighbourhoods.geojson", "r") as geo:
#     neighbourhood_geojson = json.load(geo)
# with open("A1_geo\\transit-gtfs-routes.geojson", "r") as geo:
#     routes_geojson = json.load(geo)
# with open("A1_geo\\transit_data.geojson", "r") as geo:
#     transit_data_geojson = json.load(geo)


fig = go.Figure(go.Densitymapbox(
    # mode = "markers",
    lon = clean.Longitude,
    lat = clean.Latitude,
    z=clean.counts,
    radius=15
    # marker = {'size': 3, 'color': "cyan"}
    ))

fig.update_layout(
    height=600,
    mapbox = {
        'style': "stamen-terrain",
        'center': {"lat": 44.227860, "lon": -76.496938},
        'zoom': 10,
        # 'layers': [
        #         {
        #             'visible': True,
        #             'source': neighbourhood_geojson,
        #             'type': "fill",
        #             'below': "traces",
        #             'color': "royalblue",
        #             'opacity': 0.6
        #         },
        #         {
        #             'visible': True,
        #             'source': routes_geojson,
        #             'type': "line",
        #             'below': "traces",
        #             'color': "green",
        #             'opacity': 0.8
        #         },
        #         {
        #             'visible': True,
        #             'source': transit_data_geojson,
        #             'type': "circle",
        #             'color': "pink",
        #             'opacity': 1
        #         }
        #     ]
            },
    margin = {'l':0, 'r':0, 'b':0, 't':0})
f = go.FigureWidget(fig)

app = dash.Dash('app', server=server)

app.scripts.config.serve_locally = False
dcc._js_dist[0]['external_url'] = 'https://cdn.plot.ly/plotly-basic-latest.min.js'

app.layout = html.Div([
    html.H1('Transit Data Heatmap'),
    dcc.Graph(id='my-graph', figure=f)
], className="container")


if __name__ == '__main__':
    app.run_server()


