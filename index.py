import requests
from dash import Dash,dcc,Output,Input,html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta


with open("boroughs.geojson","r") as geo:
    boroughs_geo=json.load(geo)
for feature in boroughs_geo["features"]:
    feature["properties"]["borough"] = feature["properties"]["BoroName"].upper()

url='https://data.cityofnewyork.us/resource/5uac-w243.json' #url of api
sevenMADate=(datetime.now() - relativedelta(months=7)).strftime("%Y-%m-%dT00:00:00.000")
limit=50000
offset=0
all_data=[]
while True: #getting all data into dataframe
    params={#Parameters of data i'm getting from api
        "$select":"cmplnt_fr_dt,law_cat_cd,boro_nm",
        "$where":f"cmplnt_fr_dt>='{sevenMADate}'",
        "$limit":limit,
        "$offset":offset,
        "$order":"cmplnt_fr_dt ASC"
    }
    response=requests.get(url,params=params)
    batch=response.json()
    if not batch:
        break
    all_data.extend(batch)
    offset+=limit
datafr=pd.DataFrame(all_data)
app=Dash(__name__,external_stylesheets=[dbc.themes.COSMO])
mytext=dcc.Markdown(children='')
mygraph=dcc.Graph(figure={})
monthSlider=dcc.Slider(
            max=7,
            min=4,
            step=1,
            value=4,
            marks={
                4: "5 months ago → now",
                5: "4 months ago → now",
                6: "3 months ago → now",
                7: "2 months ago → now"
            }
        )
dropdown=dcc.Dropdown(options=("All","Felony","Misdemeanor","Violation"),
                      value="All",
                      clearable=False)

app.layout=html.Div([
    dbc.Row([
        dbc.Col([html.H1("Crime statistics in NY",className="text-center")],width=6)
    ],justify='center'),
    dbc.Row([
        dbc.Col([html.H3(mytext,className="text-center")],width=6)
    ],justify='center'),
    dbc.Row([
        dbc.Col([mygraph],width=12,className="graph")
    ],justify='center'),
    dbc.Row([
        dbc.Col([monthSlider],width=8,className="month-slider")
    ],justify='center'),
    dbc.Row([
        dbc.Col([dropdown],width=6)
    ],justify='center'),
    dbc.Row([
        dbc.Col([html.P("Keep in mind that crime reports are published to the API about a month after they occur, so the last option on the slider might not be fully up to date.")],width=6)
    ],justify='center')
])
@app.callback(
    Output(mytext,'children'),
    Output(mygraph,'figure'),
    Input(dropdown,'value'),
    Input(monthSlider,'value')
)
def update_graph(cat,month):
    filtered=datafr
    filterdate = (datetime.now() - relativedelta(months=9 - month)).strftime("%Y-%m-%dT00:00:00.000")
    filtered = filtered[filtered["cmplnt_fr_dt"] >= filterdate]
    if cat!="All":
        filtered=filtered[filtered["law_cat_cd"]==cat.upper()]
    grouped = filtered.groupby("boro_nm").size().reset_index(name="Number of complaints")
    fig=px.choropleth(grouped,
                        geojson=boroughs_geo,
                        locations="boro_nm",
                        featureidkey="properties.borough",
                        color="Number of complaints",
                        color_continuous_scale="Reds",
                        projection="mercator",
                        hover_name="boro_nm",
                        hover_data={"Number of complaints":True,"boro_nm":False}

                        )
    fig.update_geos(
        lonaxis_range=[-74.3, -73.7],  # Longitude range covering NYC area
        lataxis_range=[40.5, 40.95]  # Latitude range covering NYC area

    )
    return cat,fig

if __name__=='__main__':
    app.run_server(port=8052)