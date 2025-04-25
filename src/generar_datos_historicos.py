import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import os

# Parámetros
num_registros_diarios = 5  # Número de registros a generar por día
equipos = ["CATERPILLAR 797F", "CATERPILLAR 988H", "CATERPILLAR 24M", "KOMATSU 930-E4",
           "KOMATSU 930E-4SE", "KOMATSU 980 E5", "KOMATSU 930 E3", "KOMATSU 930 E4", "KOMATSU 930 E5",
           "KOMATSU 950 E3", "CAEX", "KOMATSU 950 E4", "KOMATSU 960 E2-K"]
componentes = ["MANDO FINAL", "TRANSMISIÓN", "DIFERENCIAL DEL", "MOTOR", "SISTEMA HIDRAULICO",
               "MANDO FINAL TRA.DER", "MANDO FINAL TRA.IZQ", "MASA DERECHA", "MASA IZQUIERDA",
               "MOTOR TRACCION IZQ", "MOTOR TRACCION DER", "DIFERENCIAL TRA"]
nflota = ["911", "912", "913", "914", "915", "511", "512", "513", "515", "RT1", "RT2", "RT3", "RT4", "G126", "G127", "G128", "G129"]
cambioLubricanate = ["Muestreo", "Cambio Aceite"]

# Asociación de componentes con aceites lubricantes
componentes_aceites = {
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

# Variables globales para mantener el estado correlativo
NUM_MUESTRA_LETRAS = "ABCDE"
NUM_MUESTRA_DIGITOS = 0  # Inicializar en 0 (comenzará en 1)
NUM_REGISTRO = 0  # Inicializar en 0 (comenzará en 1)

# Función para leer el estado actual desde un archivo (si existe)
def cargar_estado():
    global NUM_MUESTRA_DIGITOS, NUM_REGISTRO
    try:
        with open("data/estado_generador.txt", "r") as f:
            lineas = f.readlines()
            if len(lineas) >= 2:
                NUM_MUESTRA_DIGITOS = int(lineas[0].strip())
                NUM_REGISTRO = int(lineas[1].strip())
            else:
                NUM_MUESTRA_DIGITOS = 0
                NUM_REGISTRO = 0
    except FileNotFoundError:
        NUM_MUESTRA_DIGITOS = 0
        NUM_REGISTRO = 0

# Función para guardar el estado actual en un archivo
def guardar_estado():
    with open("data/estado_generador.txt", "w") as f:
        f.write(f"{NUM_MUESTRA_DIGITOS}\n")
        f.write(f"{NUM_REGISTRO}\n")

# Función para generar criticidad basada en probabilidades
def generar_criticidad():
    criticidades = ["Normal"] * 65 + ["Atencion"] * 20 + ["Critico"] * 15
    return np.random.choice(criticidades)

# Función para ajustar valores según la criticidad asignada
def ajustar_valores(row):
    criticidad = row["Criticidad"]
    if criticidad == "Normal":
        row["Silicio (Si) ppm"] = np.random.randint(0, 15)
        row["Hierro (Fe) ppm"] = np.random.randint(0, 100)
        row["Aluminio (Al) ppm"] = np.random.randint(0, 10)
        row["Cobre (Cu) ppm"] = np.random.randint(0, 15)
        row["TAN mg KOH/g"] = np.round(np.random.uniform(0, 2.0), 2)
        row["Residuo Ferroso Total mg/kg"] = np.random.randint(0, 200)
    elif criticidad == "Atencion":
        row["Silicio (Si) ppm"] = np.random.randint(15, 25)
        row["Hierro (Fe) ppm"] = np.random.randint(100, 200)
        row["Aluminio (Al) ppm"] = np.random.randint(10, 20)
        row["Cobre (Cu) ppm"] = np.random.randint(15, 30)
        row["TAN mg KOH/g"] = np.round(np.random.uniform(2.0, 3.0), 2)
        row["Residuo Ferroso Total mg/kg"] = np.random.randint(200, 500)
    elif criticidad == "Critico":
        row["Silicio (Si) ppm"] = np.random.randint(25, 50)
        row["Hierro (Fe) ppm"] = np.random.randint(200, 300)
        row["Aluminio (Al) ppm"] = np.random.randint(20, 30)
        row["Cobre (Cu) ppm"] = np.random.randint(30, 50)
        row["TAN mg KOH/g"] = np.round(np.random.uniform(3.0, 4.0), 2)
        row["Residuo Ferroso Total mg/kg"] = np.random.randint(500, 600)
    return row

# Función para generar datos aleatorios con distribución de criticidad controlada
def generar_datos_historicos(fecha_inicio, fecha_fin):
    global NUM_MUESTRA_DIGITOS, NUM_REGISTRO
    cargar_estado()

    # Crear un rango de fechas entre la fecha inicial y la fecha final
    rango_fechas = pd.date_range(start=fecha_inicio, end=fecha_fin, freq='D')

    datos = {
        "Fecha": [],
        "Equipo": [],
        "Componente": [],
        "Aceite Lubricante": [],
        "nflota": [],
        "cambioLubricanate": [],
        "Contenido de agua %": [],
        "Punto de inflamacion °C": [],
        "Glicol %": [],
        "Nitracion A/cm": [],
        "Oxidación A/cm": [],
        "Hollín %": [],
        "Sulfatacion A/cm": [],
        "Diesel %": [],
        "N de part >4µm": [],
        "N° de part >6µm": [],
        "N° de part>14µm": [],
        "Código ISO 4406": [],
        "Viscosidad 100°C cSt(mm2/s)": [],
        "Viscosidad 40°C cSt(mm2/s)": [],
        "TAN mg KOH/g": [],
        "TBN mg KOH/g": [],
        "Plata (Ag) ppm": [],
        "Aluminio (Al) ppm": [],
        "Bario (Ba) ppm": [],
        "Boro (B) ppm": [],
        "Calcio (Ca) ppm": [],
        "Cromo (Cr) ppm": [],
        "Cobre (Cu) ppm": [],
        "Hierro (Fe) ppm": [],
        "Potasio (K) ppm": [],
        "Magnesio (Mg) ppm": [],
        "Molibdeno (Mo) ppm": [],
        "Sodio (Na) ppm": [],
        "Níquel (Ni) ppm": [],
        "Plomo (Pb) ppm": [],
        "Fósforo (P) ppm": [],
        "Silicio (Si) ppm": [],
        "Estaño (Sn) ppm": [],
        "Titanio (Ti) ppm": [],
        "Vanadio (V) ppm": [],
        "Zinc (Zn) ppm": [],
        "Residuo Ferroso Total mg/kg": [],
        "Numero Muestra": [],
        "Numero Registro": [],
        "Numero Serie Equipo": []
    }

    for fecha in rango_fechas:
        for _ in range(num_registros_diarios):
            letra_muestra = np.random.choice(list(NUM_MUESTRA_LETRAS))
            NUM_MUESTRA_DIGITOS += 1
            numero_muestra = f"{letra_muestra}{NUM_MUESTRA_DIGITOS:05d}"
            NUM_REGISTRO += 1
            numero_registro = f"{NUM_REGISTRO:07d}"
            numero_serie_equipo = f"LAJ{np.random.randint(0, 1000):03d}"

            componente_seleccionado = np.random.choice(list(componentes_aceites.keys()))
            aceite_lubricante = componentes_aceites[componente_seleccionado]

            datos["Fecha"].append(fecha)
            datos["Equipo"].append(np.random.choice(equipos))
            datos["Componente"].append(componente_seleccionado)
            datos["Aceite Lubricante"].append(aceite_lubricante)
            datos["nflota"].append(np.random.choice(nflota))
            datos["cambioLubricanate"].append(np.random.choice(cambioLubricanate))
            datos["Contenido de agua %"].append(np.round(np.random.uniform(0, 1), 2))
            datos["Punto de inflamacion °C"].append(np.random.randint(180, 250))
            datos["Glicol %"].append(np.round(np.random.uniform(0, 0.5), 2))
            datos["Nitracion A/cm"].append(np.random.randint(0, 5))
            datos["Oxidación A/cm"].append(np.random.randint(0, 5))
            datos["Hollín %"].append(np.round(np.random.uniform(0, 2), 2))
            datos["Sulfatacion A/cm"].append(np.random.randint(0, 5))
            datos["Diesel %"].append(np.round(np.random.uniform(0, 1), 2))
            datos["N de part >4µm"].append(np.random.randint(1000, 10000))
            datos["N° de part >6µm"].append(np.random.randint(500, 5000))
            datos["N° de part>14µm"].append(np.random.randint(100, 1000))
            datos["Código ISO 4406"].append(f"{np.random.randint(18, 22)}/{np.random.randint(16, 20)}/{np.random.randint(13, 17)}")
            datos["Viscosidad 100°C cSt(mm2/s)"].append(np.round(np.random.uniform(10, 20), 2))
            datos["Viscosidad 40°C cSt(mm2/s)"].append(np.round(np.random.uniform(80, 120), 2))
            datos["TAN mg KOH/g"].append(np.round(np.random.uniform(0, 3), 2))
            datos["TBN mg KOH/g"].append(np.random.randint(0, 10))
            datos["Plata (Ag) ppm"].append(np.random.randint(0, 5))
            datos["Aluminio (Al) ppm"].append(np.random.randint(0, 30))
            datos["Bario (Ba) ppm"].append(np.random.randint(0, 10))
            datos["Boro (B) ppm"].append(np.random.randint(0, 10))
            datos["Calcio (Ca) ppm"].append(np.random.randint(0, 1000))
            datos["Cromo (Cr) ppm"].append(np.random.randint(0, 10))
            datos["Cobre (Cu) ppm"].append(np.random.randint(0, 50))
            datos["Hierro (Fe) ppm"].append(np.random.randint(0, 300))
            datos["Potasio (K) ppm"].append(np.random.randint(0, 10))
            datos["Magnesio (Mg) ppm"].append(np.random.randint(0, 10))
            datos["Molibdeno (Mo) ppm"].append(np.random.randint(0, 10))
            datos["Sodio (Na) ppm"].append(np.random.randint(0, 30))
            datos["Níquel (Ni) ppm"].append(np.random.randint(0, 10))
            datos["Plomo (Pb) ppm"].append(np.random.randint(0, 10))
            datos["Fósforo (P) ppm"].append(np.random.randint(0, 10))
            datos["Silicio (Si) ppm"].append(np.random.randint(0, 50))
            datos["Estaño (Sn) ppm"].append(np.random.randint(0, 10))
            datos["Titanio (Ti) ppm"].append(np.random.randint(0, 10))
            datos["Vanadio (V) ppm"].append(np.random.randint(0, 10))
            datos["Zinc (Zn) ppm"].append(np.random.randint(0, 100))
            datos["Residuo Ferroso Total mg/kg"].append(np.random.randint(0, 600))
            datos["Numero Muestra"].append(numero_muestra)
            datos["Numero Registro"].append(numero_registro)
            datos["Numero Serie Equipo"].append(numero_serie_equipo)

    guardar_estado()
    df = pd.DataFrame(datos)
    df["Criticidad"] = [generar_criticidad() for _ in range(len(df))]
    df = df.apply(ajustar_valores, axis=1)
    return df

# Función para guardar datos en el archivo CSV
def guardar_datos(df_nuevos, archivo="data/datos_generados.csv"):
    os.makedirs(os.path.dirname(archivo), exist_ok=True)
    try:
        df_existente = pd.read_csv(archivo)
        df_final = pd.concat([df_existente, df_nuevos], ignore_index=True)
    except FileNotFoundError:
        df_final = df_nuevos
    df_final.to_csv(archivo, index=False)

# Bucle principal
if __name__ == "__main__":
    fecha_inicio = datetime(2022, 1, 1)  # Fecha inicial
    fecha_fin = datetime.now()  # Fecha actual
    print("Generando datos históricos...")
    df_historicos = generar_datos_historicos(fecha_inicio, fecha_fin)
    guardar_datos(df_historicos)
    print("Datos históricos generados y guardados.")