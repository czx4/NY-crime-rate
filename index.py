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
fiveYADate=(datetime.now() - relativedelta(months=4)).strftime("%Y-%m-%dT00:00:00.000") #y=1 for test
limit=50000
offset=0
all_data=[]
while True:
    params={#Parameters of data i'm getting from api
        "$select":"cmplnt_fr_dt,law_cat_cd,boro_nm",
        "$where":f"cmplnt_fr_dt>='{fiveYADate}'",
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
        dbc.Col([dropdown],width=6)
    ],justify='center')
])
@app.callback(
    Output(mytext,'children'),
    Output(mygraph,'figure'),
    Input(dropdown,'value')
)
def update_graph(cat):
    filtered=datafr
    if cat!="All":
        filtered=datafr[datafr["law_cat_cd"]==cat.upper()]
    grouped = filtered.groupby("boro_nm").size().reset_index(name="Number of complaints")
    print(grouped)
    fig=px.choropleth(grouped,
                        geojson=boroughs_geo,
                        locations="boro_nm",
                        featureidkey="properties.borough",
                        color="Number of complaints",
                        animation_frame="year",
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