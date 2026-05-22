import streamlit as st
import geopandas as gpd
import pandas as pd
import folium
from streamlit_folium import st_folium
from shapely.geometry import Polygon

st.set_page_config(layout="wide")

st.title("Mapa de Periculosidade do Rio de Janeiro")

st.write(
    "Este mapa exibe um score fictício de periculosidade "
    "para alguns bairros do Rio de Janeiro."
)

# ---------------------------
# Dados fictícios
# ---------------------------

data = {
    'nome_bairro': [
        'Copacabana',
        'Tijuca',
        'Santa Teresa',
        'Barra da Tijuca',
        'Leblon',
        'Botafogo',
        'Centro',
        'Jacarepaguá'
    ],
    'perigo_score': [7.5, 6.2, 5.8, 4.1, 3.5, 5.0, 7.0, 6.5]
}

polygons = [
    Polygon([(-43.19, -22.97), (-43.18, -22.96), (-43.17, -22.97)]),
    Polygon([(-43.25, -22.93), (-43.24, -22.92), (-43.23, -22.93)]),
    Polygon([(-43.19, -22.93), (-43.18, -22.92), (-43.17, -22.93)]),
    Polygon([(-43.38, -23.01), (-43.37, -23.00), (-43.36, -23.01)]),
    Polygon([(-43.22, -22.99), (-43.21, -22.98), (-43.20, -22.99)]),
    Polygon([(-43.19, -22.95), (-43.18, -22.94), (-43.17, -22.95)]),
    Polygon([(-43.18, -22.91), (-43.17, -22.90), (-43.16, -22.91)]),
    Polygon([(-43.34, -22.96), (-43.33, -22.95), (-43.32, -22.96)])
]

geo_rj = gpd.GeoDataFrame(
    data,
    geometry=polygons,
    crs="EPSG:4326"
)

# ---------------------------
# Mapa
# ---------------------------

map_center = [-22.9068, -43.1729]

m = folium.Map(
    location=map_center,
    zoom_start=11
)

folium.Choropleth(
    geo_data=geo_rj.to_json(),
    name='Periculosidade',
    data=geo_rj,
    columns=['nome_bairro', 'perigo_score'],
    key_on='feature.properties.nome_bairro',
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Score de Periculosidade'
).add_to(m)

folium.GeoJson(
    geo_rj,
    tooltip=folium.GeoJsonTooltip(
        fields=['nome_bairro', 'perigo_score'],
        aliases=['Bairro:', 'Score:']
    )
).add_to(m)

folium.LayerControl().add_to(m)

# ---------------------------
# Exibir mapa
# ---------------------------

st_folium(m, width=1200, height=700)
