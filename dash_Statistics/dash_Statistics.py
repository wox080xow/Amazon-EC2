import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
application = app.server

df_env = pd.read_csv("data/EnvironmentalVar.csv")
df_eco = pd.read_csv("data/EconomicVar.csv")
df_house = pd.read_csv("data/HouseVar.csv")
available_indicators = df_env.columns
available_indicators1 = df_eco.columns
available_indicators2 = df_house.columns
# layout
app.layout = html.Div([
    html.Div([
            html.H1('環境變數相關圖',style={'text-align':'center','color':'#0000FF'}),
        html.Div([
            html.H5("請選擇x軸環境變數"),
            #下拉式篩選器設定
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='警察局'
            ),
        ],
        style={'width': '20%', 'display': 'inline-block'}),

        html.Div([
            html.H5("請選擇y軸環境變數"),

            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='犯罪數'
            ),
        ],
        style={'width': '20%', 'float': 'right', 'display': 'inline-block'}),

    dcc.Graph(id='indicator-graphic')]),
    html.Div([],style={'height': '400px'}),


    html.Div([
            html.H1('經濟變數相關圖',style={'text-align':'center','color':'#9900FF'}),
        html.Div([
            html.H5("請選擇經濟變數"),

            dcc.Dropdown(
                id='xaxis-column1',
                options=[{'label': i, 'value': i} for i in available_indicators1],
                value='所得收入總計'
            ),
        ],
        style={'width': '20%', 'display': 'inline-block'}),

    dcc.Graph(id='indicator-graphic1'),
    html.Div([],style={'height': '300px'}),

    html.Div([
            html.H1('房屋特性',style={'text-align':'center','color':'#00FF00'}),
        html.Div([
            html.H5("請選擇房屋特性"),

            dcc.Dropdown(
                id='xaxis-column2',
                options=[{'label': i, 'value': i} for i in available_indicators2],
                value='房間數'
            ),
        ],
        style={'width': '20%', 'display': 'inline-block'}),

    dcc.Graph(id='indicator-graphic2'),
       ])
    ])
])

# callback
@app.callback(
    dash.dependencies.Output('indicator-graphic', 'figure'),
    dash.dependencies.Input('xaxis-column', 'value'),
    dash.dependencies.Input('yaxis-column', 'value'))
def update_graph(xaxis_column_name, yaxis_column_name):

    fig = px.scatter(x=df_env[xaxis_column_name],
                     y=df_env[yaxis_column_name], text = df_env['地區'],size = df_env[xaxis_column_name],color= df_env[yaxis_column_name])

    fig.update_traces(textposition='top center')

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest',font_size=16)

    fig.update_xaxes(title=xaxis_column_name)

    fig.update_yaxes(title=yaxis_column_name)

    return fig

@app.callback(
    dash.dependencies.Output('indicator-graphic1', 'figure'),
    dash.dependencies.Input('xaxis-column1', 'value'))
def update_graph(xaxis_column_name):

    fig = px.bar(x=df_eco[xaxis_column_name], y=df_eco['地區'],color_discrete_sequence=['#00DDDD'])

    fig.update_xaxes(title=xaxis_column_name)
    fig.update_layout(yaxis={'categoryorder':'total ascending'},font_size=16)

    return fig

@app.callback(
    dash.dependencies.Output('indicator-graphic2', 'figure'),
    dash.dependencies.Input('xaxis-column2', 'value'))
def update_graph(xaxis_column_name):

    if xaxis_column_name == '樓層數' :
        range1 = [-1,20]
    else:
        range1 = [-1,6]

    fig = px.histogram(x=df_house[xaxis_column_name],range_x=range1,range_y=[-1000,max(df_house.groupby(xaxis_column_name).count().iloc[:,:1].values.tolist())[0]*1.1],color_discrete_sequence=['#FF0000'],width=1600,height=700)
    fig.update_xaxes(title=xaxis_column_name)

    fig.update_layout(yaxis={'categoryorder':'total ascending'},font_size=16)

    return fig

if __name__ == '__main__':
    application.run(host = '0.0.0.0', debug = True, port = 8054)
