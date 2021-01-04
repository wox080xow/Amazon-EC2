import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
from textwrap import dedent

df = pd.read_csv('AreaPredto2021.csv')
df['Date'] = pd.to_datetime(df['Date'], infer_datetime_format=True)
df['value'] = df['value'].astype('int')

# Dash app
app = dash.Dash(__name__)
application = app.server

app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})


app.layout = html.Div([
    html.H1('台北市房價預測'),
    dcc.Markdown("請選擇所欲查詢地區"),

    dcc.Dropdown(
        id='Area-dropdown',
        options=[{'label': i, 'value': i} for i in df.Area.unique()],
        multi=True,
        value=['Songshan']),

    dcc.Graph(id='timeseries-graph')

])

@app.callback(
    dash.dependencies.Output('timeseries-graph', 'figure'),
    dash.dependencies.Input('Area-dropdown', 'value'))

def update_graph(Area_values):
    dff = df.loc[df['Area'].isin(Area_values)]
    
    return {
        'data': [go.Scatter(
            x=dff[dff['Area'] == Area]['Date'],
            y=dff[dff['Area'] == Area]['value'],

            mode='lines+markers',
            name=Area,
            marker={
                'size': 7,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        ) for Area in dff.Area.unique()],
        
        'layout': go.Layout(
#             title="House Price over time, by Area",
            xaxis={'title': '日期'},
            yaxis={'title': '房屋價格(萬/坪)'},
            margin={'l': 60, 'b': 50, 't': 80, 'r': 0},
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    application.run(host = '0.0.0.0', debug = True, port = 8052)

