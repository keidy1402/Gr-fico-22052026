import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página do Streamlit
st.set_page_config(
    page_title="Dashboard de Ocorrências",
    page_icon="🗺️",
    layout="wide"
)

# Título do Dashboard
st.title("📌 Análise de Ocorrências por Município (2026)")
st.markdown("Visualize a distribuição geográfica das ocorrências de forma interativa.")

# 1. Carregar os dados
@st.cache_data # Cache para o app carregar muito mais rápido
def carregar_dados():
    df = pd.read_csv('ocorrencias_geolocalizadas_final.csv', sep=';', encoding='utf-8-sig')
    return df.dropna(subset=['latitude', 'longitude'])

df = carregar_dados()

# 2. Filtros na Barra Lateral (Sidebar)
st.sidebar.header("Filtros")
ufs_disponiveis = sorted(df['UF'].unique())
ufs_selecionadas = st.sidebar.multiselect(
    "Selecione os Estados (UF):",
    options=ufs_disponiveis,
    default=ufs_disponiveis # Começa com todos selecionados
)

# Filtrar o dataframe com base na seleção do usuário
df_filtrado = df[df['UF'].isin(ufs_selecionadas)]

# 3. Métricas de Destaque
total_ocorrencias = int(df_filtrado['TOTAL'].sum())
total_municipios = df_filtrado['MUNICIPIO'].nunique()

col1, col2 = st.columns(2)
with col1:
    st.metric(label="Total de Ocorrências", value=f"{total_ocorrencias:,}".replace(",", "."))
with col2:
    st.metric(label="Municípios Atendidos", value=total_municipios)

st.markdown("---")

# 4. Criação do Gráfico Scattergeo
if not df_filtrado.empty:
    fig = px.scatter_geo(
        df_filtrado,
        lat='latitude',
        lon='longitude',
        size='TOTAL',
        color='TOTAL',
        hover_name='MUNICIPIO',
        hover_data={'UF': True, 'TOTAL': True, 'latitude': False, 'longitude': False},
        color_continuous_scale=px.colors.sequential.Reds,
        size_max=35
    )

    # Configuração do mapa focado no Brasil
    fig.update_geos(
        scope='south america',
        showcountries=True,
        countrycolor="Black",
        showland=True, 
        landcolor="#e8ece9", # Um tom cinza claro mais moderno para o Streamlit
        showocean=True,
        oceancolor="#cbdcf7",
        center=dict(lat=-14.2350, lon=-51.9253),
        projection_scale=4
    )

    fig.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0},
        height=650
    )

    # 5. Exibir o gráfico no Streamlit
    st.plotly_chart(fig, use_container_width=True)
    
    # 6. Tabela de dados (Opcional - para o usuário ver os top municípios)
    st.subheader("📋 Dados Detalhados (Top 10 Municípios)")
    top_10 = df_filtrado.sort_values(by='TOTAL', ascending=False).head(10)[['MUNICIPIO', 'UF', 'TOTAL']]
    st.dataframe(top_10, use_container_width=True)
else:
    st.warning("Nenhum estado selecionado. Por favor, escolha pelo menos um na barra lateral.")
