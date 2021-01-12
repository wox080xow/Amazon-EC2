import pandas as pd

# 準備捷運站相關資料
df = pd.read_csv("./dash_20201226/OKMRTExit1.csv")
df_lng = df['經度'].astype('str').tolist()
df_lat = df['緯度'].astype('str').tolist()
df_name = df['出入口名稱'].astype('str').tolist()

# 準備公車站相關資料
df2 = pd.read_csv("./dash_20201226/OKBusStation.csv")
df2_lng = df2['經度'].astype('str').tolist()
df2_lat = df2['緯度'].astype('str').tolist()
df2_name = df2['properties.bsm_chines'].astype('str').tolist()

# 準備醫療機構資料
def hospital(file_addr):
    result = pd.read_csv(file_addr)
    return result.iloc[:,0:3]

def hospital2(file_addr):
    result = pd.read_csv(file_addr, encoding = 'big5')
    return result.iloc[:,0:3]

hospital_df = pd.concat([hospital("./dash_20201226/台北市診所清冊1090926(含經緯度).csv"), hospital("./dash_20201226/台北市醫院清冊1090926(含經緯度).csv")], axis = 0)
# hospital_df = pd.concat([hospital_df, hospital2("./dash_20201226/臺北市藥局清冊(含經緯度) (1).csv")], axis = 0)

# 準備教育機構
education_1 = pd.read_csv("./dash_20201226/taipeiPrivateSchool00.csv")
education_1 = education_1.iloc[:,1:4]
education_2 = pd.read_csv("./dash_20201226/taipeiPublicKindergarten00.csv")
education_2 = education_2.iloc[:,0:3]
education_3 = pd.read_csv("./dash_20201226/taipeiPublicSchool.csv")
education_3 = education_3.iloc[:,0:3]
education_df = pd.concat([education_2,education_1], axis = 0)

# 準備政府機構
gov_df = pd.read_csv("./dash_20201226/taipeiGovermentAgencyOnly.csv")
gov_df = gov_df.iloc[:,0:3]

# 各行政區資料準備
area_df = pd.read_csv("./dash_20201226/merge_df.csv")
area_df = area_df.set_index('行政區')

# Main App
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

app = dash.Dash(__name__)
application = app.server

app.layout = html.Div([
    html.Div([
        html.H2(children='台北市重要機關地圖', style = {
            'font-family':'微軟正黑體'
        }),
        html.P(children='請點選地圖右側的圖示，來篩選您需要的台北市機構，謝謝', style = {
            'font-family':'微軟正黑體',
            'font-size':'14px'
        }),
        dcc.Graph(
            id='gapminder',
            figure={
                'data': [
                    go.Scattermapbox(
                        lat=df_lat,
                        lon=df_lng,
                        mode='markers',
                        name="捷運站",
                        marker=go.scattermapbox.Marker(
                size = 10, color='orange', symbol='rail-metro'
            ),
            text = df_name,
            ),
                    go.Scattermapbox(
                        lat = df2_lat,
                        lon = df2_lng,
                        mode = 'markers',
                        name="公車站牌",
                        marker = go.scattermapbox.Marker(
                size = 7, color='red',symbol='bus'
            ),
            text = df2_name,
            ),
            go.Scattermapbox(
                        lat=hospital_df['Latitude'],
                        lon=hospital_df['Longitude'],
                        mode='markers',
                        name="醫療機構",
                        marker=go.scattermapbox.Marker(
                size = 7, color='blue', symbol='hospital'
            ),
            text = hospital_df['機構名稱'],
            ),
            go.Scattermapbox(
                        lat=education_df['Latitude'],
                        lon=education_df['Longtitude'],
                        mode='markers',
                        name="私立教育機構",
                        marker=go.scattermapbox.Marker(
                size = 10, color='green', symbol='school'
            ),
            text = education_df['Name'],
            ),
            go.Scattermapbox(
                        lat=gov_df['Latitude'],
                        lon=gov_df['Longtitude'],
                        mode='markers',
                        name="公家機構與學校",
                        marker=go.scattermapbox.Marker(
                size = 10, color='purple', symbol='police'
            ),
            text = gov_df['Name'],
            )
                ],
                'layout': go.Layout(
                    autosize=True,
                    hovermode='closest',
                    margin=dict(
                        l=20,
                        r=20,
                        b=20,
                        t=20
                    ),
                    mapbox=dict(
                        accesstoken='pk.eyJ1IjoiZXJpa3NvbjA2MTEiLCJhIjoiY2tpeTRib3RnMTd6dTJ5c2Joa3diZXVqcyJ9.2Qtsf3xtMppGs5lwXvDvyw',
                        bearing = 0,
                        center = dict(lat=25.03767065815624,lon=121.50812738115941),
                        pitch = 0,
                        style = 'light',
                        zoom = 17
                ))
            }
        )
            ]),
    html.Div([
        html.H2("台北市區域資料", style = {
            'font-family':'微軟正黑體'
        }),
        dcc.Dropdown(
            id='demo-dropdown',
            options=[
                {'label': '中正區', 'value': '中正區'},
                {'label': '大安區', 'value': '大安區'},
                {'label': '信義區', 'value': '信義區'},
                {'label': '中山區', 'value': '中山區'},
                {'label': '大同區', 'value': '大同區'},
                {'label': '松山區', 'value': '松山區'},
                {'label': '內湖區', 'value': '內湖區'},
                {'label': '文山區', 'value': '文山區'},
                {'label': '萬華區', 'value': '萬華區'},
                {'label': '北投區', 'value': '北投區'},
                {'label': '士林區', 'value': '士林區'},
                {'label': '南港區', 'value': '南港區'}
            ],
                value='中正區'),
        html.Table([
        html.Tr([html.Td(['總人口數']), html.Td(id='output1')]),
        html.Tr([html.Td(['人口密度']), html.Td(id='output2')]),
        html.Tr([html.Td(['公車站數量']), html.Td(id='output3')]),
        html.Tr([html.Td(['捷運站數量']), html.Td(id='output4')]),
        html.Tr([html.Td(['醫院數量']), html.Td(id='output5')]), #hospitalCount
        html.Tr([html.Td(['政府機關數量']), html.Td(id='output6')]),# govCount
        html.Tr([html.Td(['人均所得總額']), html.Td(id='output7')]),
        ]),
    ])
])

def area(string):
    return area_df[str(string)][value]

@app.callback(
    dash.dependencies.Output('output1', 'children'),
    dash.dependencies.Output('output2', 'children'),
    dash.dependencies.Output('output3', 'children'),
    dash.dependencies.Output('output4', 'children'),
    dash.dependencies.Output('output5', 'children'),
    dash.dependencies.Output('output6', 'children'),
    dash.dependencies.Output('output7', 'children'),
    dash.dependencies.Input('demo-dropdown', 'value'))
def update_output(value):
    output1 = area_df['總人口數'][value]
    output2 = area_df['人口密度'][value]
    output3 = area_df['busCount'][value]
    output4 = area_df['subwayCount'][value]
    output5 = area_df['hospitalCount'][value]
    output6 = area_df['govCount'][value]
    output7 = area_df['所得總額'][value]
    return output1, output2, output3, output4, output5, output6, output7


if __name__ == '__main__':
    application.run(host = '0.0.0.0', debug = True, port = 8051)
