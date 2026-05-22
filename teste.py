import streamlit as st
import plotly.graph_objects as go
import pandas as pd

df = pd.read_csv('https://github.com/keidy1402/Gr-fico-22052026/blob/72fb9948cf422874cd2dc27332161eb5a41638f1/OCORRENCIAS_2026.csv%20(1).xlsx')
df.head()

# Configuração Streamlit
# ---------------------------------
st.set_page_config(page_title="Mapa de Periculosidade", layout="wide")

st.title("Mapa de Periculosidade no Brasil")

st.write("Visualização de regiões com maior índice de perigo.")

trace = go.Scattergeo(
                     locationmode = 'Brazil',
                     lon = df['lon'],
                     lat = df['lat'],
                     text = df['name'] + '- População: ' + df['pop'].astype(str),
                     marker = dict(
                            size = df['pop']/5000,
                            color = '#e74c3c',
                            line = {'width': 0.5,
                                    'color': '#2c3e50'},
                            sizemode = 'area')
                    )
data = [trace]

layout = go.Layout(
        title = '<b>População americana em 2014</b>',
        titlefont = {'family': 'Arial',
                     'size': 24},
        geo =  {'scope': 'usa',
                'projection': {'type': 'albers usa'},
                'showland': True,
                'landcolor': '#2ecc71',
                'showlakes': True,
                'lakecolor': '#3498db',
                'subunitwidth': 1,
                'subunitcolor': "rgb(255, 255, 255)"
                })

fig = go.Figure(data=data, layout=layout)
fig.show()

# ---------------------------------
# Mostrar no Streamlit
# ---------------------------------
st.plotly_chart(fig, use_container_width=True)
