import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

st.set_page_config(
    page_title="Dashboard Tribológico",
    layout="wide",
    page_icon="📊",
    initial_sidebar_state="expanded"
)

############################### Modelo Machine Learning ################################################
# Cargar el modelo entrenado
@st.cache_resource
def cargar_modelo():
    return joblib.load("data/modelo_entrenado.joblib")

modelo = cargar_modelo()

# Cargar los nombres de características
@st.cache_resource
def cargar_feature_names():
    return joblib.load("data/feature_names.joblib")

feature_names = cargar_feature_names()

# Función para hacer predicciones
def predecir_criticidad(datos):
    # Codificar las variables categóricas
    datos_encoded = pd.get_dummies(datos).reindex(columns=feature_names, fill_value=0)
    # Hacer la predicción
    prediccion = modelo.predict(datos_encoded)
    return prediccion

# Función para generar valores automáticos de minerales y otros parámetros
def generar_valores_automaticos(equipo, componente, aceite_lubricante):
    # Definir rangos típicos basados en el equipo, componente y aceite lubricante
    valores_generados = {
        "Viscosidad 100°C cSt(mm2/s)": np.round(np.random.uniform(10, 20), 2),
        "TAN mg KOH/g": np.round(np.random.uniform(0, 4), 2),
        "TBN mg KOH/g": np.random.randint(0, 10),
        "Silicio (Si) ppm": np.random.randint(0, 50),
        "Hierro (Fe) ppm": np.random.randint(0, 300),
        "Aluminio (Al) ppm": np.random.randint(0, 30),
        "Cobre (Cu) ppm": np.random.randint(0, 50),
        "Cromo (Cr) ppm": np.random.randint(0, 10),
        "Níquel (Ni) ppm": np.random.randint(0, 10),
        "Residuo Ferroso Total mg/kg": np.random.randint(0, 600),
        "Contenido de Partículas Sólidas mg/L": np.random.randint(0, 100),
        "Índice de Oxidación": np.random.randint(0, 5)
    }
    return valores_generados

# Interfaz de usuario para hacer predicciones
st.subheader("Predicción Automática de Criticidad")

# Equipos generados en el script
equipos = [
    "CATERPILLAR 797F", "CATERPILLAR 988H", "CATERPILLAR 24M", "KOMATSU 930-E4",
    "KOMATSU 930E-4SE", "KOMATSU 980 E5", "KOMATSU 930 E3", "KOMATSU 930 E4", "KOMATSU 930 E5",
    "KOMATSU 950 E3", "CAEX", "KOMATSU 950 E4", "KOMATSU 960 E2-K"
]
equipo = st.selectbox("Selecciona Equipo:", equipos)

# Componentes generados en el script
componentes = [
    "MANDO FINAL", "TRANSMISIÓN", "DIFERENCIAL DEL", "MOTOR", "SISTEMA HIDRAULICO",
    "MANDO FINAL TRA.DER", "MANDO FINAL TRA.IZQ", "MASA DERECHA", "MASA IZQUIERDA",
    "MOTOR TRACCION IZQ", "MOTOR TRACCION DER", "DIFERENCIAL TRA"
]
componente = st.selectbox("Selecciona Componente:", componentes)

# Aceites Lubricantes asociados a los componentes
aceites_lubricantes = {
    "MANDO FINAL": "MOBIL MOBILTRANS HD 30",
    "TRANSMISIÓN": "MOBIL MOBILTRANS HD 30",
    "DIFERENCIAL DEL": "MOBIL MOBILTRANS HD 30",
    "MOTOR": "MOBIL DELVAC 15W40",
    "SISTEMA HIDRAULICO": "MOBIL DTE 24",
    "MANDO FINAL TRA.DER": "MOBIL MOBILTRANS HD 30",
    "MANDO FINAL TRA.IZQ": "MOBIL MOBILTRANS HD 30",
    "MASA DERECHA": "MOBIL MOBILTRANS HD 30",
    "MASA IZQUIERDA": "MOBIL MOBILTRANS HD 30",
    "MOTOR TRACCION IZQ": "MOBIL SHC GEAR 680",
    "MOTOR TRACCION DER": "MOBIL SHC GEAR 680",
    "DIFERENCIAL TRA": "MOBIL MOBILTRANS HD 30"
}
aceite_lubricante = aceites_lubricantes.get(componente, "No especificado")
st.write(f"Aceite Lubricante: {aceite_lubricante}")

# Generar valores automáticos
valores_generados = generar_valores_automaticos(equipo, componente, aceite_lubricante)
st.write("Valores Generados Automáticamente:")
st.json(valores_generados)

# Crear un DataFrame con los datos generados
input_data = pd.DataFrame({
    "Equipo": [equipo],
    "Componente": [componente],
    "Aceite Lubricante": [aceite_lubricante],
    **{k: [v] for k, v in valores_generados.items()}
})

# Botón para predecir
if st.button("Predecir"):
    prediccion = predecir_criticidad(input_data)
    st.success(f"Nivel de Criticidad Predicho: {prediccion[0]}")
######################################### Fin Modelo de ML ###################################


# Configurar la página


# Estilo personalizado para un diseño más elegante
st.markdown("""
<style>
/* Cambiar el color de fondo principal */
.stApp {
    background-color: #FF6F00; /* Fondo naranja vibrante */
    color: #FFFFFF; /* Texto blanco para contraste */
}

/* Cambiar el color de los títulos */
h1, h2, h3, h4, h5, h6 {
    color: #FFFFFF; /* Texto blanco para los títulos */
    font-family: 'Arial', sans-serif; /* Fuente clara y profesional */
    font-weight: bold; /* Asegurar que los títulos sean prominentes */
}

/* Cambiar el color de los widgets (botones) */
div.stButton > button {
    background-color: #FF6F00; /* Naranja vibrante */
    color: white; /* Texto blanco para contraste */
    border-radius: 5px; /* Bordes redondeados para un diseño moderno */
    border: none; /* Sin bordes adicionales */
    font-weight: bold; /* Texto en negrita para mayor visibilidad */
    transition: background-color 0.3s ease; /* Efecto suave al pasar el mouse */
}
div.stButton > button:hover {
    background-color: #E65C00; /* Un tono más oscuro de naranja al pasar el mouse */
}

/* Cambiar el color de los selectores */
.stSelectbox > div > div {
    background-color: #FF6F00; /* Fondo naranja */
    color: #FFFFFF; /* Texto blanco */
    border: 1px solid #CCCCCC; /* Borde sutil para definir los límites */
    border-radius: 5px; /* Bordes redondeados */
}

/* Cambiar el color de los inputs de texto */
.stTextInput > div > div > input {
    background-color: #FF6F00; /* Fondo naranja */
    color: #FFFFFF; /* Texto blanco */
    border: 1px solid #CCCCCC; /* Borde sutil */
    border-radius: 5px; /* Bordes redondeados */
}

/* Cambiar el color de las tablas */
.stDataFrame > div > table {
    background-color: #FF6F00; /* Fondo naranja */
    color: #FFFFFF; /* Texto blanco */
    border: 1px solid #CCCCCC; /* Borde sutil */
    border-radius: 5px; /* Bordes redondeados */
}

/* Cambiar el color de los sliders */
.stSlider > div > div > div {
    background-color: #FF6F00; /* Fondo naranja */
    color: #FFFFFF; /* Texto blanco */
    border-radius: 5px; /* Bordes redondeados */
}

/* Cambiar el color del sidebar */
[data-testid="stSidebar"] {
    background-color: #000000; /* Fondo negro para el sidebar */
    color: #FFFFFF; /* Texto blanco para contraste */
}

/* Cambiar el color de los títulos del sidebar */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #FFFFFF; /* Texto blanco para los títulos del sidebar */
}

/* Cambiar el color de los widgets en el sidebar */
[data-testid="stSidebar"] .stButton > button {
    background-color: #FF6F00; /* Naranja vibrante */
    color: white; /* Texto blanco */
    border-radius: 5px; /* Bordes redondeados */
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
    criticidad_seleccionada = st.sidebar.multiselect("Selecciona Nivel de Criticidad:", df["Criticidad"].unique())

    # Filtrar datos
    df_filtrado = df
    if equipo_seleccionado:
        df_filtrado = df_filtrado[df_filtrado["Equipo"].isin(equipo_seleccionado)]
    if componente_seleccionado:
        df_filtrado = df_filtrado[df_filtrado["Componente"].isin(componente_seleccionado)]
    if criticidad_seleccionada:
        df_filtrado = df_filtrado[df_filtrado["Criticidad"].isin(criticidad_seleccionada)]

    # Mostrar datos filtrados (colapsable)
    with st.expander("🎯 Datos Filtrados"):
        st.dataframe(df_filtrado)

    # Indicador de Semáforo
    st.markdown("#### 🚦 Indicador de Semáforo")
    nivel_residuo_ferroso = df_filtrado["Residuo Ferroso Total mg/kg"].mean()
    if nivel_residuo_ferroso < 200:
        st.success("🟢 Condiciones Normales")
    elif 200 <= nivel_residuo_ferroso < 400:
        st.warning("🟡 Nivel de Precaución")
    else:
        st.error("🔴 Nivel Crítico")

    # Visualizaciones
    st.subheader("📊 Visualizaciones")

    # Crear columnas para organizar los gráficos
    col1, col2 = st.columns(2)

    # Gráfico de Barras: Desgaste por Hierro
    with col1:
        st.markdown("#### 📊 Desgaste por Hierro (ppm)")
        fig, ax = plt.subplots(figsize=(5, 3))
        sns.barplot(
            data=df_filtrado,
            x="Componente",
            y="Hierro (Fe) ppm",
            hue="Componente",
            legend=False,
            palette="Blues_d",
            ax=ax
        )
        ax.set_title("Desgaste Promedio por Hierro", fontsize=10, color="#003366")
        ax.set_xlabel("Componente", fontsize=8)
        ax.set_ylabel("Hierro (ppm)", fontsize=8)
        ax.tick_params(axis='x', rotation=45)
        st.pyplot(fig)

    # Gráfico de Barras: Concentración de Silicio
    with col2:
        st.markdown("#### 📊 Concentración de Silicio (ppm)")
        fig, ax = plt.subplots(figsize=(5, 3))
        sns.barplot(
            data=df_filtrado,
            x="Componente",
            y="Silicio (Si) ppm",
            hue="Componente",
            legend=False,
            palette="Greens_d",
            ax=ax
        )
        ax.set_title("Concentración Promedio de Silicio", fontsize=10, color="#003366")
        ax.set_xlabel("Componente", fontsize=8)
        ax.set_ylabel("Silicio (ppm)", fontsize=8)
        ax.tick_params(axis='x', rotation=45)
        st.pyplot(fig)

    # Gráfico de Tendencia de Viscosidad
    with col1:
        st.markdown("#### 📈 Tendencia de Viscosidad")
        fig, ax = plt.subplots(figsize=(5, 3))
        df_filtrado['Fecha'] = pd.to_datetime(df_filtrado['Fecha'])
        df_agrupado = (
            df_filtrado.groupby([pd.Grouper(key="Fecha", freq="W"), "Componente"])
            .mean(numeric_only=True)
            .reset_index()
        )
        sns.lineplot(
            data=df_agrupado,
            x="Fecha",
            y="Viscosidad 100°C cSt(mm2/s)",
            hue="Componente",
            palette="viridis",
            ax=ax
        )
        ax.set_title("Tendencia de Viscosidad", fontsize=10, color="#003366")
        ax.set_xlabel("Fecha", fontsize=8)
        ax.set_ylabel("Viscosidad", fontsize=8)
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True, linestyle="--", alpha=0.5)
        st.pyplot(fig)

    # Gráfico de Distribución de Residuo Ferroso
    with col2:
        st.markdown("#### 📊 Distribución de Residuo Ferroso")
        fig, ax = plt.subplots(figsize=(5, 3))
        df_residuo = df_filtrado[df_filtrado["Residuo Ferroso Total mg/kg"] > 0]
        sns.histplot(
            data=df_residuo,
            x="Residuo Ferroso Total mg/kg",
            hue="Componente",
            multiple="stack",
            palette="Blues_d",
            bins=10,
            ax=ax
        )
        ax.set_title("Distribución de Residuo Ferroso", fontsize=10, color="#003366")
        ax.set_xlabel("Residuo Ferroso (mg/kg)", fontsize=8)
        ax.set_ylabel("Frecuencia", fontsize=8)
        ax.tick_params(axis='x', rotation=45)
        st.pyplot(fig)

    # Gráfico de Proporción de Niveles de Criticidad
    with col1:
        st.markdown("#### 📊 Proporción de Niveles de Criticidad")
        fig, ax = plt.subplots(figsize=(4, 3))
        criticidad_counts = df_filtrado["Criticidad"].value_counts()
        colors = ["#2ca02c", "#ff7f0e", "#d62728"]
        ax.pie(
            criticidad_counts,
            labels=criticidad_counts.index,
            autopct="%1.1f%%",
            startangle=90,
            colors=colors
        )
        ax.set_title("Proporción de Criticidad", fontsize=10, color="#003366")
        st.pyplot(fig)

    # Gráfico de TAN vs TBN
    with col2:
        st.markdown("#### 📊 Comparación de TAN y TBN")
        fig, ax = plt.subplots(figsize=(5, 3))
        sns.scatterplot(
            data=df_filtrado,
            x="TAN mg KOH/g",
            y="TBN mg KOH/g",
            hue="Componente",
            palette="Set2",
            s=50,
            ax=ax
        )
        ax.set_title("Comparación de TAN y TBN", fontsize=10, color="#003366")
        ax.set_xlabel("TAN (mg KOH/g)", fontsize=8)
        ax.set_ylabel("TBN (mg KOH/g)", fontsize=8)
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True, linestyle="--", alpha=0.5)
        st.pyplot(fig)

    # Gráfico de Contenido de Agua
    with col1:
        st.markdown("#### 📊 Distribución del Contenido de Agua")
        fig, ax = plt.subplots(figsize=(5, 3))
        sns.boxplot(
            data=df_filtrado,
            x="Componente",
            y="Contenido de agua %",
            hue="Componente",
            palette="Set3",
            legend=False,
            ax=ax
        )
        ax.set_title("Contenido de Agua", fontsize=10, color="#003366")
        ax.set_xlabel("Componente", fontsize=8)
        ax.set_ylabel("Agua (%)", fontsize=8)
        ax.tick_params(axis='x', rotation=45)
        st.pyplot(fig)

    # Gráfico de Criticidad por Equipo
    with col2:
        st.markdown("#### 📊 Criticidad por Equipo")
        criticidad_por_equipo = (
            df_filtrado.groupby(["Equipo", "Criticidad"]).size().unstack(fill_value=0)
        )
        fig, ax = plt.subplots(figsize=(6, 4))
        criticidad_por_equipo.plot(kind="bar", stacked=True, ax=ax, color=["#ff7f0e", "#d62728", "#2ca02c"])
        ax.set_title("Criticidad por Equipo", fontsize=10, color="#003366")
        ax.set_xlabel("Equipo", fontsize=8)
        ax.set_ylabel("Cantidad", fontsize=8)
        ax.tick_params(axis='x', rotation=45)
        ax.legend(title="Criticidad", fontsize=8)
        st.pyplot(fig)

    # Gráfico de Criticidad por Aceite Lubricante
    with col1:
        st.markdown("#### 📊 Criticidad por Aceite Lubricante")
        criticidad_por_aceite = (
            df_filtrado.groupby(["Aceite Lubricante", "Criticidad"]).size().unstack(fill_value=0)
        )
        fig, ax = plt.subplots(figsize=(6, 4))
        criticidad_por_aceite.plot(kind="bar", stacked=True, ax=ax, color=["#ff7f0e", "#d62728", "#2ca02c"])
        ax.set_title("Criticidad por Aceite Lubricante", fontsize=10, color="#003366")
        ax.set_xlabel("Aceite Lubricante", fontsize=8)
        ax.set_ylabel("Cantidad", fontsize=8)
        ax.tick_params(axis='x', rotation=45)
        ax.legend(title="Criticidad", fontsize=8)
        st.pyplot(fig)