import pandas as pd
df = pd.read_csv("./done_data/subway_result.csv")
df_lng = df['經度'].astype('str').tolist()
df_lat = df['緯度'].astype('str').tolist()
df_name = df['出入口名稱'].astype('str').tolist()

df2 = pd.read_csv("./done_data/bus_result.csv")
df2_lng = df2['經度'].astype('str').tolist()
df2_lat = df2['緯度'].astype('str').tolist()
df2_name = df2['properties.bsm_chines'].astype('str').tolist()

def hospital(file_addr):
    result = pd.read_csv(file_addr, encoding = 'big5')
    return result.iloc[:,0:3]

hospital_df = pd.concat([hospital("./data/台北市診所清冊1090926(含經緯度).csv"), hospital("./data/台北市醫院清冊1090926(含經緯度).csv")], axis = 0)
hospital_df = pd.concat([hospital_df, hospital("./data/臺北市藥局清冊.csv")], axis = 0)

education_1 = pd.read_csv("./data/taipeiPrivateSchool00.csv")
education_1 = education_1.iloc[:,1:4]
education_2 = pd.read_csv("./data/taipeiPublicKindergarten00.csv")
education_2 = education_2.iloc[:,0:3]
education_df = pd.concat([education_2,education_1], axis = 0)

gov_df = pd.read_csv("./data/taipeiGovernmentAgency01.csv")
gov_df = gov_df.iloc[:,0:3]

house_df = pd.read_csv('./done_data/predOutcome.csv', index_col=None)
house_df = house_df[house_df['year']==2020]

house_area_mean = house_df.groupby('Area').mean()

area_df = pd.read_csv("./done_data/merge_df.csv")
area_df = area_df.set_index('Area')

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import re

app = dash.Dash(__name__)
application = app.server

df = pd.DataFrame({
    "Category": ["Population", "Denm", "Bananas", "Apples", "Bananas", "Capital"],
    "Amount": [40000, 10000, 20000, 20000, 40000, 50000]
})

fig = px.bar(df, x="Category", y="Amount", barmode="group")

table_head = '150px' #設定表格的縮排

app.layout = html.Div([
    html.Div([
        html.H1(children='台北市中古屋模型預測', style = {
        }),
        html.P(children='請選擇右邊的圖示，篩選您想要了解的物件周邊設施', style = {
            'font-size':'16px'
        }),
        html.P(children='Taipei officially Taipei City, is the capital and a special municipality of Taiwan. Located in Northern Taiwan, Taipei City is an enclave of the municipality of New Taipei City that sits about 25 km southwest of the northern port city of Keelung. Most of the city rests on the Taipei Basin, an ancient lakebed. The basin is bounded by the relatively narrow valleys of the Keelung and Xindian rivers, which join to form the Tamsui River', style = {
            'font-size':'12px'
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
                size = 5, color='orange', symbol='rail-metro'
            ),
            text = df_name,
            ),
                    go.Scattermapbox(
                        lat = df2_lat,
                        lon = df2_lng,
                        mode = 'markers',
                        name="公車站",
                        marker = go.scattermapbox.Marker(
                size = 5, color='red',symbol='bus'
            ),
            text = df2_name,
            ),
            go.Scattermapbox(
                        lat=hospital_df['Latitude'],
                        lon=hospital_df['Longitude'],
                        mode='markers',
                        name="醫療中心",
                        marker=go.scattermapbox.Marker(
                size = 5, color='blue', symbol='hospital'
            ),
            text = hospital_df['機構名稱'],
            ),
            go.Scattermapbox(
                        lat=education_df['Latitude'],
                        lon=education_df['Longtitude'],
                        mode='markers',
                        name="私立機構與學校",
                        marker=go.scattermapbox.Marker(
                size = 5, color='green', symbol='school'
            ),
            text = education_df['Name'],
            ),
            go.Scattermapbox(
                        lat=gov_df['Latitude'],
                        lon=gov_df['Longtitude'],
                        mode='markers',
                        name="公立機構與學校",
                        marker=go.scattermapbox.Marker(
                size = 5, color='purple', symbol='police'
            ),
            text = gov_df['Name'],
            ),
            # 加入中古屋的資料
            go.Scattermapbox(
                        lat=house_df['Latitude'],
                        lon=house_df['Lontitude'],
                        mode='markers',
                        name="中古屋位置",
                        marker=go.scattermapbox.Marker(
                size = 15, color='orange'
            ),
            text = house_df['Address'],
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
                    center = dict(lat=25.03374536000858,lon=121.54328512547893),
                    pitch = 0,
                    zoom = 15
                    )) #layoutend
                }) # figure end
            ]), #div end
    html.Div([ #information div
        html.Div([
            html.H2("行政區基本資料"),
            html.P(id='area_out'),
            html.Table([
                html.Tr([html.Td(['區域人口'],style={'width':table_head}), html.Td(id='output1')]),
                html.Tr([html.Td(['人口密度'],style={'width':table_head}), html.Td(id='output2')]),
                html.Tr([html.Td(['公車站牌數'],style={'width':table_head}), html.Td(id='output3')]),
                html.Tr([html.Td(['捷運站數'],style={'width':table_head}), html.Td(id='output4')]),
                html.Tr([html.Td(['區內醫院數'],style={'width':table_head}), html.Td(id='output5')]), #hospitalCount
                html.Tr([html.Td(['政府機關數'],style={'width':table_head}), html.Td(id='output6')]),# govCount
                html.Tr([html.Td(['人均年所得'],style={'width':table_head}), html.Td(id='output7')])
                        ])
                    ],style={'width':'50%','display': 'inline-block', 'vertical-align': 'top'}),
        html.Div([
            html.H2("房屋基本資料"),
            html.P(id='hover-data'),
            html.Table([
                html.Tr([html.Td(['建物型態'],style={'width':table_head}), html.Td(id='house_out1')]),
                html.Tr([html.Td(['廳數'],style={'width':table_head}), html.Td(id='house_out2')]),
                html.Tr([html.Td(['房間數'],style={'width':table_head}), html.Td(id='house_out3')]),
                html.Tr([html.Td(['衛浴數'],style={'width':table_head}), html.Td(id='house_out4')]),
                html.Tr([html.Td(['隔間'],style={'width':table_head}), html.Td(id='house_out5')]), 
                html.Tr([html.Td(['管理組織'],style={'width':table_head}), html.Td(id='house_out6')])
                        ]),
            ],style={'width':'50%', 'display': 'inline-block', 'vertical-align': 'top'})
    ]),

    dcc.Graph(
        id='example-graph'
        )

], style={'marginLeft': '25%', 'marginRight': '25%', 'font-family':'微軟正黑體'})


@app.callback(
    dash.dependencies.Output('area_out', 'children'),
    dash.dependencies.Output('output1', 'children'),
    dash.dependencies.Output('output2', 'children'),
    dash.dependencies.Output('output3', 'children'),
    dash.dependencies.Output('output4', 'children'),
    dash.dependencies.Output('output5', 'children'),
    dash.dependencies.Output('output6', 'children'),
    dash.dependencies.Output('output7', 'children'),
    dash.dependencies.Input('gapminder', 'clickData'))
def update_output(hoverData):
    if hoverData is None:
        return '請選擇中古屋圖示','None','None','None','None','None','None', 'None'
    else:
        address = hoverData['points'][0]['text']
        try:
            result_match = re.search(r'(.{2}\u5340)', address)
            value = result_match[0]
            output1 = area_df['總人口數'][value]
            output2 = area_df['人口密度'][value]
            output3 = area_df['busCount'][value]
            output4 = area_df['subwayCount'][value]
            output5 = area_df['hospitalCount'][value]
            output6 = area_df['govCount'][value]
            output7 = area_df['所得總額'][value]
            return "你的行政區為：{}".format(value), output1, output2, output3, output4, output5, output6, output7
        except:
            return '請選擇中古屋圖示','None','None','None','None','None','None', 'None'

@app.callback(
    dash.dependencies.Output('hover-data', 'children'),
    dash.dependencies.Output('house_out1', 'children'),
    dash.dependencies.Output('house_out2', 'children'),
    dash.dependencies.Output('house_out3', 'children'),
    dash.dependencies.Output('house_out4', 'children'),
    dash.dependencies.Output('house_out5', 'children'),
    dash.dependencies.Output('house_out6', 'children'),
    dash.dependencies.Input('gapminder', 'clickData'))
def display_hover_data(hover_data):
    if hover_data is None:
        return '請選擇一個中古屋地址', None, None, None, None, None, None
    else:
        location = hover_data['points'][0]['text']
        house_row = house_df[house_df['Address'] == location]
        try:
            house_out1 = house_row['建物型態'].tolist()[0]
            house_out2 = house_row['廳數'].tolist()[0]
            house_out3 = house_row['房間數'].tolist()[0]
            house_out4 = house_row['衛浴數'].tolist()[0]
            house_out5 = house_row['隔間'].tolist()[0]
            house_out6 = house_row['管理組織'].tolist()[0]
            return "你目前位於：{}".format(location), house_out1, house_out2, house_out3, house_out4, house_out5, house_out6
        except:
            return "你目前位於：{}".format(location), 'None', 'None', 'None', 'None', 'None', 'None'


@app.callback(
    dash.dependencies.Output("example-graph", "figure"), 
    dash.dependencies.Input('gapminder', 'clickData'))

def update_bar_chart(hover_data):
    if hover_data is None:
        df = pd.DataFrame({
              "Area": ["地區", "地區", "地區", "物件", "物件", "物件"],
              "Catgory": ["單價元坪", "總價元", "總坪數", "單價元坪", "總價元", "總坪數"],
              "Number": [0,0,0,0,0,0]
        })
        fig = px.bar(df,x="Catgory", y="Number", color="Area", barmode="group")
        return fig
    else:
        location = hover_data['points'][0]['text']
        try:
            house_row = house_df[house_df['Address'] == location]
            result_match = re.search(r'(.{2}\u5340)', location)
            area = result_match[0]
            area_row = house_area_mean[house_area_mean.index == area]
            # set 價格變數
            area_perprice = area_row['單價元坪'][0]
            area_totalprice = area_row['總價元'][0]
            area_totalsize = area_row['總坪數'][0]
            house_perprice = house_row['單價元坪'].tolist()[0]
            house_totalprice = house_row['總價元'].tolist()[0]
            house_totalsize = house_row['總坪數'].tolist()[0]
            pred_perprice = house_row['pred'].tolist()[0]
            df = pd.DataFrame({
                  "分類": ["地區平均", "地區平均", "地區平均", "實際成交", "實際成交", "實際成交","模型預測"],
                  "交易資訊": ["每坪單價", "總價元", "總坪數", "每坪單價", "總價元", "總坪數","每坪單價"],
                  "金額": [area_perprice,area_totalprice/20,area_totalsize*30000,house_perprice,house_totalprice/20,house_totalsize*30000,pred_perprice]
            })
            fig = px.bar(df,x="交易資訊", y="金額", color="分類", barmode="group", 
                         text = ['{} 萬元'.format(round(area_perprice/10000,1)),
                                 '{} 萬元'.format(round(area_totalprice/10000,1)),
                                 '{} 坪'.format(round(area_totalsize,1)),
                                 '{} 萬元'.format(round(house_perprice/10000,1)),
                                 '{} 萬元'.format(round(house_totalprice/10000,1)),
                                 '{} 坪'.format(round(house_totalsize,1)),
                                 '{} 萬元'.format(round(pred_perprice/10000,1))] )
            return fig
        except:
            df = pd.DataFrame({
                  "Area": ["地區平均", "地區平均", "地區平均", "物件", "物件", "物件"],
                  "Catgory": ["單價元坪", "總價元", "總坪數", "單價元坪", "總價元", "總坪數"],
                  "Number": [0,0,0,0,0,0]
            })
            fig = px.bar(df,x="Catgory", y="Number", color="Area", barmode="group")
            return fig




if __name__ == '__main__':
    application.run(host = '0.0.0.0', debug = True, port = 8053)
