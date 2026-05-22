import streamlit as st
import pandas as pd
import plotly.express as px
import json
import requests

# ---------------------------------
# Ler Excel
# ---------------------------------

df = pd.read_excel("OCORRENCIAS_2026.csv.csv")

# ---------------------------------
# Agrupar ocorrências
# ---------------------------------

ocorrencias = df.groupby("uf").size().reset_index(name="total")

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
    locations="uf",
    featureidkey="properties.sigla",
    color="total",
    color_continuous_scale="Reds",
    projection="mercator",
    hover_name="uf",
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
