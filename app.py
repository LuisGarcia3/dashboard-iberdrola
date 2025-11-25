import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# --------------------------- #
# CONFIGURACIÓN DE LA PÁGINA
# --------------------------- #
st.set_page_config(
    page_title="Dashboard Alertas Iberdrola",
    layout="wide",
    page_icon="⚡"
)

# --------------------------- #
# ESTILO GLOBAL IBERDROLA
# --------------------------- #
st.markdown("""
<style>
    /* Fondo y texto */
    .main, .block-container {
        background-color: #F5F7F3 !important;
        color: #004B8D !important;
        font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
    }
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #E6EFDE !important;
        color: #004B8D !important;
        padding: 20px;
    }
    /* Títulos */
    h1, h2, h3 {
        font-weight: 800 !important;
        color: #004B8D !important;
    }
    /* Botones */
    .stButton>button {
        background-color: #6AB547 !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 10px 25px !important;
        font-weight: 700 !important;
        border: none !important;
    }
    .stButton>button:hover {
        background-color: #4C8A32 !important;
    }
    /* Selectbox y multiselect */
    div[role="listbox"] > div {
        border: 1px solid #6AB547 !important;
        border-radius: 6px !important;
        color: #004B8D !important;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------- #
# TÍTULO
# --------------------------- #
st.title("Dashboard de Alertas de Compliance – Iberdrola")

# --------------------------- #
# DATOS SIMULADOS (Para probar sin CSV)
# --------------------------- #
np.random.seed(42)

# Crear un dataframe simulado con columnas similares
fechas = pd.date_range(start="2024-01-01", end="2024-06-30", freq="D")
n = len(fechas) * 10

df = pd.DataFrame({
    "FechaHora": np.random.choice(fechas, n),
    "AlertaCompliance": np.random.choice([True, False], n, p=[0.3, 0.7]),
    "MotivoAlerta": np.random.choice([
        "SWIFT Alto Riesgo",
        "Egreso de Riesgo sin Ejecutivo Asignado",
        "Puntuación de Riesgo Extrema (>90)",
        "Transacción Inusual",
        "Otros"
    ], n)
})

df["Mes"] = df["FechaHora"].dt.to_period("M").astype(str)

# Filtramos solo alertas activas
df_alerts = df[df["AlertaCompliance"]]

# --------------------------- #
# FILTROS
# --------------------------- #
st.sidebar.header("Filtros")
st.sidebar.markdown("Usa los filtros para explorar patrones de alertas.")

lista_meses = sorted(df_alerts["Mes"].unique())
filtro_mes = st.sidebar.multiselect("Seleccionar Mes", lista_meses, default=lista_meses)

lista_motivos = sorted(df_alerts["MotivoAlerta"].unique())
filtro_motivo = st.sidebar.multiselect("Motivo de la Alerta", lista_motivos, default=lista_motivos)

df_filtrado = df_alerts[
    (df_alerts["Mes"].isin(filtro_mes)) &
    (df_alerts["MotivoAlerta"].isin(filtro_motivo))
]

# --------------------------- #
# GRÁFICA: Alertas por Mes
# --------------------------- #
st.header("Frecuencia Mensual de Alertas")

alertas_mensuales = df_filtrado.groupby("Mes").size().reset_index(name="ConteoAlertas")

fig = px.bar(
    alertas_mensuales,
    x="Mes",
    y="ConteoAlertas",
    text="ConteoAlertas",
    title="Número de Alertas por Mes",
    labels={"Mes": "Mes", "ConteoAlertas": "Número de Alertas"},
    color="ConteoAlertas",
    color_continuous_scale=["#6AB547", "#F39C12", "#004B8D"],
)

fig.update_traces(textposition="outside", marker_line_color="#004B8D", marker_line_width=1.5)
fig.update_layout(
    plot_bgcolor="#F5F7F3",
    paper_bgcolor="#F5F7F3",
    font_color="#004B8D",
    xaxis_title="Mes",
    yaxis_title="Número de Alertas",
    yaxis=dict(dtick=1),
    margin=dict(t=50, b=50)
)

st.plotly_chart(fig, use_container_width=True)

if st.button("Mostrar Tabla de Alertas por Mes"):
    st.dataframe(alertas_mensuales)

# --------------------------- #
# PATRONES DETECTADOS
# --------------------------- #
st.header("Patrones Detectados")

if st.checkbox("Ver SWIFT de Alto Riesgo"):
    patron_swift = df_filtrado[df_filtrado["MotivoAlerta"].str.contains("SWIFT", na=False)]
    st.dataframe(patron_swift)

if st.checkbox("Ver Egreso sin Ejecutivo Asignado"):
    patron_sin_ejecutivo = df_filtrado[df_filtrado["MotivoAlerta"] == "Egreso de Riesgo sin Ejecutivo Asignado"]
    st.dataframe(patron_sin_ejecutivo)

if st.checkbox("Ver Puntuación de Riesgo Extrema"):
    patron_riesgo_extremo = df_filtrado[df_filtrado["MotivoAlerta"] == "Puntuación de Riesgo Extrema (>90)"]
    st.dataframe(patron_riesgo_extremo)

st.markdown("---")

# --------------------------- #
# VISUALIZACIONES 3D (iframe)
# --------------------------- #
st.header("Visualizaciones 3D")
st.markdown("Selecciona un modelo 3D para visualizarlo dentro del dashboard.")

sites_3d = {
    "Modelo 3D - Sitio 1": "https://cheerful-croquembouche-cfc9bd.netlify.app/",
    "Modelo 3D - Sitio 2": "https://superlative-kleicha-c9c31a.netlify.app/",
    "Modelo 3D - Sitio 3": "https://jolly-bubblegum-f1baa6.netlify.app/",
    "Modelo 3D - Sitio 4": "https://curious-entremet-041122.netlify.app/"
}

selected_3d = st.selectbox("Selecciona un modelo 3D:", list(sites_3d.keys()))

st.components.v1.iframe(
    src=sites_3d[selected_3d],
    width=1200,
    height=800,
    scrolling=True
)

st.markdown("---")
st.caption("© Dashboard Iberdrola – Universidad Rosario Castellanos | Integración con gráficos 3D externos.")