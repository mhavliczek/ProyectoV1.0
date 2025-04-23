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

# Aplicar estilos personalizados
st.markdown("""
<style>
/* Estilo global */
.stApp {
    background-color: #FF6F00; /* Fondo naranja vibrante */
    color: #FFFFFF; /* Texto blanco para contraste */
}

/* Títulos */
h1, h2, h3, h4, h5, h6 {
    color: #FFFFFF; /* Texto blanco para los títulos */
    font-family: 'Arial', sans-serif;
    font-weight: bold;
}

/* Botones */
div.stButton > button {
    background-color: #FF6F00; /* Naranja vibrante */
    color: white;
    border-radius: 5px;
    border: none;
    font-weight: bold;
    transition: background-color 0.3s ease;
}
div.stButton > button:hover {
    background-color: #E65C00; /* Un tono más oscuro de naranja al pasar el mouse */
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #000000; /* Fondo negro para el sidebar */
    color: #FFFFFF; /* Texto blanco para contraste */
}
</style>
""", unsafe_allow_html=True)

# Encabezado con logo
st.markdown("""
<div style="display: flex; align-items: center; justify-content: center; margin-bottom: 20px;">
    <img src="https://via.placeholder.com/150" alt="Logo" style="width: 150px; height: auto;">
</div>
""", unsafe_allow_html=True)

# Título principal
st.markdown("<h1 style='text-align: center;'>Bienvenido a la Universidad de las Américas</h1>", unsafe_allow_html=True)

# Slider Hero (usando st.selectbox para simular un slider)
st.markdown("<h2 style='text-align: center;'>Descubre nuestras áreas destacadas</h2>", unsafe_allow_html=True)

# Opciones del slider
slides = {
    "Innovación": "https://via.placeholder.com/800x400?text=Innovación",
    "Educación": "https://via.placeholder.com/800x400?text=Educación",
    "Investigación": "https://via.placeholder.com/800x400?text=Investigación",
}

# Crear un selectbox para cambiar entre slides
selected_slide = st.selectbox("Selecciona una categoría:", list(slides.keys()))

# Mostrar la imagen correspondiente al slide seleccionado
st.image(slides[selected_slide], use_column_width=True)

# Contenido adicional
st.markdown("<h3 style='text-align: center;'>Nuestros Servicios</h3>", unsafe_allow_html=True)
st.write("""
Ofrecemos una amplia gama de servicios educativos y tecnológicos para potenciar tu futuro.
""")

# Botón de acción
if st.button("¡Conoce más aquí!"):
    st.write("Gracias por tu interés. Pronto nos comunicaremos contigo.")

# Sidebar con información adicional
st.sidebar.markdown("<h2 style='text-align: center;'>Menú</h2>", unsafe_allow_html=True)
st.sidebar.write("""
- Acerca de nosotros
- Programas académicos
- Investigación
- Contacto
""")

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
            .mean()
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
            palette="Set3",
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