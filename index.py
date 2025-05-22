import requests
from dash import Dash,dcc,Output,Input
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import json

with open("boroughs.geojson","r") as geo:
    boroughs_geo=json.load(geo)
for feature in boroughs_geo["features"]:
    feature["properties"]["borough"] = feature["properties"]["BoroName"].upper()

url='https://data.cityofnewyork.us/resource/5uac-w243.json' #url of api

params={#Parameters of data i'm getting from api
    "$select":"cmplnt_fr_dt,law_cat_cd,boro_nm",
    "$where":"cmplnt_fr_dt>='2025-03-08T00:00:00'",
    "$limit":1000
}
response=requests.get(url,params=params)
if response.status_code==200: 
    data=response.json()
    datafr=pd.DataFrame(data)
else:
    print("error ",response.status_code)

app=Dash(__name__,external_stylesheets=[dbc.themes.COSMO])
mytext=dcc.Markdown(children='')
mygraph=dcc.Graph(figure={})
dropdown=dcc.Dropdown(options=("All","Felony","Misdemeanor","Violation"),
                      value="All",
                      clearable=False)

app.layout=dbc.Container([
    dbc.Row([
        dbc.Col([mytext],width=6)
    ],justify='center'),
    dbc.Row([
        dbc.Col([mygraph],width=12)
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
    filtered=datafr[datafr["law_cat_cd"]==cat.upper()]
    grouped = filtered.groupby("boro_nm").size().reset_index(name="complaints_num")
    fig=px.choropleth(grouped,
                        geojson=boroughs_geo,
                        locations="boro_nm",
                        featureidkey="properties.borough",
                        color="complaints_num",
                        color_continuous_scale="Reds",
                        projection="mercator"
                        )
    fig.update_geos(
        lonaxis_range=[-74.3, -73.7],  # Longitude range covering NYC area
        lataxis_range=[40.5, 40.95]  # Latitude range covering NYC area

    )
    return cat,fig

if __name__=='__main__':
    app.run_server(port=8052)