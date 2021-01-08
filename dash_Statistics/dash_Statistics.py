import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc

app = dash.Dash(__name__)
application = app.server

if __name__ == '__main__':
    application.run(host = '0.0.0.0', debug = True, port = 8054)
