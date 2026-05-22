import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------
# Dados de exemplo
# ---------------------------------
dados = {
    "cidade": [
        "São Paulo",
        "Rio de Janeiro",
        "Salvador",
        "Fortaleza",
        "Manaus",
        "Curitiba",
        "Brasília"
    ],
    
    "lat": [
        -23.5505,
        -22.9068,
        -12.9714,
        -3.7319,
        -3.1190,
        -25.4284,
        -15.7939
    ],
    
    "lon": [
        -46.6333,
        -43.1729,
        -38.5014,
        -38.5267,
        -60.0217,
        -49.2733,
        -47.8828
    ],
    
    # índice de periculosidade
    "periculosidade": [
        95,
        88,
        75,
        70,
        65,
        45,
        40
    ]
}

df = pd.DataFrame(dados)

# ---------------------------------
# Configuração Streamlit
# ---------------------------------
st.set_page_config(page_title="Mapa de Periculosidade", layout="wide")

st.title("Mapa de Periculosidade no Brasil")

st.write("Visualização de regiões com maior índice de perigo.")

# ---------------------------------
# Criação do mapa
# ---------------------------------
fig = px.scatter_geo(
    df,
    lat="lat",
    lon="lon",
    size="periculosidade",
    color="periculosidade",
    hover_name="cidade",
    
    # escala das bolhas
    size_max=50,

    # cores
    color_continuous_scale=[
        "#f0dbb6",
        "#c68c53",
        "#f2b856",
        "#104f7e",
        "#c03131"
    ],

    projection="natural earth"
)

# ---------------------------------
# Ajustes do mapa
# ---------------------------------
fig.update_geos(
    scope="south america",
    showcountries=True,
    countrycolor="white",
    showland=True,
    landcolor="#1DB954",  # verde do mapa
    coastlinecolor="white",
    lataxis_range=[-35, 6],
    lonaxis_range=[-75, -30]
)

fig.update_layout(
    height=700,
    margin={"r":0,"t":0,"l":0,"b":0},
    paper_bgcolor="#ebebeb"
)

# ---------------------------------
# Mostrar no Streamlit
# ---------------------------------
st.plotly_chart(fig, use_container_width=True)
