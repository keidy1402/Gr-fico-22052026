import plotly.express as px
import requests
import streamlit as st
import pandas as pd

df = pd.read_csv(
    "OCORRENCIAS_2026.csv.csv",
    sep=";",
    encoding="latin1"
)

st.write(df.columns)

st.dataframe(df.head())

# ---------------------------------
# Agrupar ocorrências
# ---------------------------------

ocorrencias = df.groupby("UF").size().reset_index(name="Total")

# ---------------------------------
# GeoJSON estados Brasil
# ---------------------------------

geojson_url = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson"

geojson = requests.get(geojson_url).json()

# ---------------------------------
# Criar mapa
# ---------------------------------

fig = px.choropleth(
    ocorrencias,
    geojson=geojson,
    locations="UF",
    featureidkey="properties.sigla",
    color="total",
    color_continuous_scale="Reds",
    projection="mercator",
    hover_name="UF",
    title="Mapa de Periculosidade por Estado"
)

fig.update_geos(
    fitbounds="locations",
    visible=False
)

# ---------------------------------
# Streamlit
# ---------------------------------

st.set_page_config(layout="wide")

st.title("Mapa de Periculosidade no Brasil")

st.plotly_chart(fig, use_container_width=True)
