import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Configurar la página
st.set_page_config(
    page_title="Dashboard Tribológico",
    layout="wide",
    page_icon="📊",
    initial_sidebar_state="expanded"
)

# Estilo personalizado para un diseño más elegante
st.markdown("""
<style>
    /* Cambiar el color de fondo */
    .stApp {
        background-color: #F5F5F5; /* Fondo claro */
    }
    /* Cambiar el color de los títulos */
    h1, h2, h3, h4, h5, h6 {
        color: #003366; /* Azul marino */
    }
    /* Cambiar el color de los widgets */
    div.stButton > button {
        background-color: #003366;
        color: white;
        border-radius: 5px;
    }
    /* Cambiar el color de los selectores */
    .stSelectbox > div > div {
        background-color: #E6F2FF; /* Azul claro */
    }
</style>
""", unsafe_allow_html=True)

# Título
st.title("📊 Dashboard de Monitoreo Análisis Tribológico")

# Función para cargar datos
@st.cache_data(ttl=60)  # Actualiza los datos cada 60 segundos
def cargar_datos():
    try:
        return pd.read_csv("data/datos_generados.csv")
    except FileNotFoundError:
        st.error("El archivo 'datos_generados.csv' no existe. Asegúrate de que el script de generación de datos esté funcionando.")
        return pd.DataFrame()

# Cargar datos
df = cargar_datos()

# Verificar si el DataFrame está vacío
if df.empty:
    st.warning("No hay datos disponibles para mostrar.")
else:
    # Mostrar vista previa de los datos completos (colapsable)
    with st.expander("📋 Datos Completos"):
        st.dataframe(df)

    # Filtros
    st.sidebar.header("🔍 Filtros")
    equipo_seleccionado = st.sidebar.multiselect("Selecciona Equipo:", df["Equipo"].unique())
    componente_seleccionado = st.sidebar.multiselect("Selecciona Componente:", df["Componente"].unique())

    # Filtrar datos
    df_filtrado = df
    if equipo_seleccionado:
        df_filtrado = df_filtrado[df_filtrado["Equipo"].isin(equipo_seleccionado)]
    if componente_seleccionado:
        df_filtrado = df_filtrado[df_filtrado["Componente"].isin(componente_seleccionado)]

    # Indicador de Semáforo (colapsable)
    with st.expander("🚦 Indicador de Semáforo"):
        nivel_residuo_ferroso = df_filtrado["Residuo Ferroso (mg/kg)"].mean()
        if nivel_residuo_ferroso < 200:
            st.success("🟢 Condiciones Normales")
        elif 200 <= nivel_residuo_ferroso < 400:
            st.warning("🟡 Nivel de Precaución")
        else:
            st.error("🔴 Nivel Crítico")

    # Mostrar datos filtrados (colapsable)
    with st.expander("🎯 Datos Filtrados"):
        st.dataframe(df_filtrado)

    # Visualizaciones
    st.subheader("📊 Visualizaciones")

    # Usar pestañas para organizar las visualizaciones
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Desgaste por Hierro",
        "Concentración de Silicio",
        "Tendencia de Viscosidad",
        "Distribución de Residuo Ferroso",
        "Relación entre Hierro y Silicio"
    ])

    # Gráfico de Barras: Desgaste por Hierro
    with tab1:
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(
            data=df_filtrado,
            x="Componente",
            y="Hierro (ppm)",
            palette="Blues_d",
            ax=ax
        )
        ax.set_title("Desgaste Promedio por Hierro", fontsize=14, color="#003366")
        ax.set_xlabel("Componente", fontsize=12)
        ax.set_ylabel("Hierro (ppm)", fontsize=12)
        st.pyplot(fig)

    # Gráfico de Barras: Concentración de Silicio
    with tab2:
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(
            data=df_filtrado,
            x="Componente",
            y="Silicio (ppm)",
            palette="Greens_d",
            ax=ax
        )
        ax.set_title("Concentración Promedio de Silicio", fontsize=14, color="#003366")
        ax.set_xlabel("Componente", fontsize=12)
        ax.set_ylabel("Silicio (ppm)", fontsize=12)
        st.pyplot(fig)

    # Gráfico de Viscosidad Mejorado
    with tab3:
        fig, ax = plt.subplots(figsize=(12, 6))

        # Agrupar los datos por semana (o mes) y componente para reducir la cantidad de puntos
        df_filtrado['Fecha'] = pd.to_datetime(df_filtrado['Fecha'])  # Asegurarse de que la columna Fecha sea datetime
        df_agrupado = (
            df_filtrado.groupby([pd.Grouper(key="Fecha", freq="W"), "Componente"])  # Agrupar por fecha y componente
            .mean()
            .reset_index()
        )

        # Gráfico de dispersión
        sns.scatterplot(
            data=df_agrupado,
            x="Fecha",
            y="Viscosidad",
            hue="Componente",  # Ahora `Componente` está disponible
            palette="viridis",
            s=100,  # Tamaño de los puntos
            ax=ax
        )

        # Personalizar el gráfico
        ax.set_title("Tendencia de Viscosidad por Semana", fontsize=14, color="#003366")
        ax.set_xlabel("Fecha", fontsize=12)
        ax.set_ylabel("Viscosidad", fontsize=12)
        ax.tick_params(axis='x', rotation=45)  # Rotar las fechas para mejor legibilidad
        ax.grid(True, linestyle="--", alpha=0.5)  # Agregar una cuadrícula
        ax.set_ylim(0, df_agrupado["Viscosidad"].max() * 1.2)  # Limitar el eje Y

        st.pyplot(fig)

    # Gráfico de Distribución de Residuo Ferroso
    with tab4:
        fig, ax = plt.subplots(figsize=(10, 5))

        # Filtrar solo los valores de residuo ferroso mayores a 0
        df_residuo = df_filtrado[df_filtrado["Residuo Ferroso (mg/kg)"] > 0]

        # Histograma
        sns.histplot(
            data=df_residuo,
            x="Residuo Ferroso (mg/kg)",
            hue="Componente",
            multiple="stack",
            palette="Blues_d",
            bins=20,
            ax=ax
        )

        # Personalizar el gráfico
        ax.set_title("Distribución de Residuo Ferroso por Componente", fontsize=14, color="#003366")
        ax.set_xlabel("Residuo Ferroso (mg/kg)", fontsize=12)
        ax.set_ylabel("Frecuencia", fontsize=12)
        ax.grid(True, linestyle="--", alpha=0.5)

        st.pyplot(fig)

    # Gráfico de Relación entre Hierro y Silicio
    with tab5:
        fig, ax = plt.subplots(figsize=(10, 6))

        # Gráfico de dispersión
        sns.scatterplot(
            data=df_filtrado,
            x="Hierro (ppm)",
            y="Silicio (ppm)",
            hue="Componente",
            palette="coolwarm",
            s=100,  # Tamaño de los puntos
            ax=ax
        )

        # Personalizar el gráfico
        ax.set_title("Relación entre Hierro y Silicio", fontsize=14, color="#003366")
        ax.set_xlabel("Hierro (ppm)", fontsize=12)
        ax.set_ylabel("Silicio (ppm)", fontsize=12)
        ax.grid(True, linestyle="--", alpha=0.5)

        st.pyplot(fig)