import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

df = pd.read_csv("./data/OKMRTExit1.csv")
df_lng = df['經度'].astype('str').tolist()
df_lat = df['緯度'].astype('str').tolist()
df_name = df['出入口名稱'].astype('str').tolist()

df2 = pd.read_csv("./data/OKBusStation.csv")
df2_lng = df2['經度'].astype('str').tolist()
df2_lat = df2['緯度'].astype('str').tolist()
df2_name = df2['properties.bsm_chines'].astype('str').tolist()

app = dash.Dash()
application = app.server

app.layout = html.Div([
    html.H2(children='A Gapminder Replica with Dash'),
    dcc.Graph(
        id='gapminder',
        figure={
            'data': [
                go.Scattermapbox(
                    lat=df_lat,
                    lon=df_lng,
                    mode='markers',
                    marker=go.scattermapbox.Marker(
            size = 10, color='orange', symbol='bus'
        ),
        text = df_name,
        ),
                go.Scattermapbox(
                    lat = df2_lat,
                    lon = df2_lng,
                    mode = 'markers',
                    marker = go.scattermapbox.Marker(
            size = 3, color='orange'
        ),
        text = df2_name,
        )
            ],
            'layout': go.Layout(
                autosize=True,
                hovermode='closest',
                mapbox=dict(
                    accesstoken='pk.eyJ1IjoiZXJpa3NvbjA2MTEiLCJhIjoiY2tpeTRib3RnMTd6dTJ5c2Joa3diZXVqcyJ9.2Qtsf3xtMppGs5lwXvDvyw',
                    bearing = 0,
                    center = dict(lat=25.063717,lon=121.552335),
                    pitch = 0,
                    zoom = 11
            ))
        }
    )
])

if __name__ == '__main__':
    application.run(host = '0.0.0.0', debug = True, port = 8050)
