import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import os

# Parámetros
num_registros = 50  # Número de registros a generar cada vez
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
            
            # Verificar que haya suficientes líneas en el archivo
            if len(lineas) >= 2:
                NUM_MUESTRA_DIGITOS = int(lineas[0].strip())
                NUM_REGISTRO = int(lineas[1].strip())
            else:
                # Si no hay suficientes líneas, inicializar con valores predeterminados
                NUM_MUESTRA_DIGITOS = 0
                NUM_REGISTRO = 0
    except FileNotFoundError:
        # Si el archivo no existe, usar valores iniciales
        NUM_MUESTRA_DIGITOS = 0
        NUM_REGISTRO = 0

# Función para guardar el estado actual en un archivo
def guardar_estado():
    with open("data/estado_generador.txt", "w") as f:
        f.write(f"{NUM_MUESTRA_DIGITOS}\n")
        f.write(f"{NUM_REGISTRO}\n")

# Función para generar criticidad basada en probabilidades
def generar_criticidad():
    # Definir las proporciones de criticidad
    criticidades = ["Normal"] * 65 + ["Atencion"] * 20 + ["Critico"] * 15
    return np.random.choice(criticidades)

# Función para ajustar valores según la criticidad asignada
def ajustar_valores(row):
    criticidad = row["Criticidad"]
    
    if criticidad == "Normal":
        # Asegurar que los valores estén dentro del rango normal
        row["Silicio (Si) ppm"] = np.random.randint(0, 15)
        row["Hierro (Fe) ppm"] = np.random.randint(0, 100)
        row["Aluminio (Al) ppm"] = np.random.randint(0, 10)
        row["Cobre (Cu) ppm"] = np.random.randint(0, 15)
        row["TAN mg KOH/g"] = np.round(np.random.uniform(0, 2.0), 2)
        row["Residuo Ferroso Total mg/kg"] = np.random.randint(0, 200)
    elif criticidad == "Atencion":
        # Ajustar valores para Atención
        row["Silicio (Si) ppm"] = np.random.randint(15, 25)
        row["Hierro (Fe) ppm"] = np.random.randint(100, 200)
        row["Aluminio (Al) ppm"] = np.random.randint(10, 20)
        row["Cobre (Cu) ppm"] = np.random.randint(15, 30)
        row["TAN mg KOH/g"] = np.round(np.random.uniform(2.0, 3.0), 2)
        row["Residuo Ferroso Total mg/kg"] = np.random.randint(200, 500)
    elif criticidad == "Critico":
        # Ajustar valores para Crítico
        row["Silicio (Si) ppm"] = np.random.randint(25, 50)
        row["Hierro (Fe) ppm"] = np.random.randint(200, 300)
        row["Aluminio (Al) ppm"] = np.random.randint(20, 30)
        row["Cobre (Cu) ppm"] = np.random.randint(30, 50)
        row["TAN mg KOH/g"] = np.round(np.random.uniform(3.0, 4.0), 2)
        row["Residuo Ferroso Total mg/kg"] = np.random.randint(500, 600)
    
    return row

# Función para generar datos aleatorios con distribución de criticidad controlada
def generar_datos_aleatorios():
    global NUM_MUESTRA_DIGITOS, NUM_REGISTRO

    # Cargar el estado actual
    cargar_estado()

    # Generar nuevos datos
    datos = {
        "Fecha": [datetime.now() + timedelta(minutes=5 * i) for i in range(num_registros)],
        "Equipo": np.random.choice(equipos, size=num_registros),
        "Componente": np.random.choice(list(componentes_aceites.keys()), size=num_registros),
        "Aceite Lubricante": [],
        "nflota": np.random.choice(nflota, size=num_registros),
        "cambioLubricanate": np.random.choice(cambioLubricanate, size=num_registros),
        "Contenido de agua %": np.round(np.random.uniform(0, 1), 2),
        "Punto de inflamacion °C": np.random.randint(180, 250, size=num_registros),
        "Glicol %": np.round(np.random.uniform(0, 0.5), 2),
        "Nitracion A/cm": np.random.randint(0, 5, size=num_registros),
        "Oxidación A/cm": np.random.randint(0, 5, size=num_registros),
        "Hollín %": np.round(np.random.uniform(0, 2), 2),
        "Sulfatacion A/cm": np.random.randint(0, 5, size=num_registros),
        "Diesel %": np.round(np.random.uniform(0, 1), 2),
        "N de part >4µm": np.random.randint(1000, 10000, size=num_registros),
        "N° de part >6µm": np.random.randint(500, 5000, size=num_registros),
        "N° de part>14µm": np.random.randint(100, 1000, size=num_registros),
        "Código ISO 4406": [f"{np.random.randint(18, 22)}/{np.random.randint(16, 20)}/{np.random.randint(13, 17)}" for _ in range(num_registros)],
        "Viscosidad 100°C cSt(mm2/s)": np.round(np.random.uniform(10, 20), 2),
        "Viscosidad 40°C cSt(mm2/s)": np.round(np.random.uniform(80, 120), 2),
        "TAN mg KOH/g": np.round(np.random.uniform(0, 3), 2),
        "TBN mg KOH/g": np.random.randint(0, 10, size=num_registros),
        "Plata (Ag) ppm": np.random.randint(0, 5, size=num_registros),
        "Aluminio (Al) ppm": np.random.randint(0, 30, size=num_registros),
        "Bario (Ba) ppm": np.random.randint(0, 10, size=num_registros),
        "Boro (B) ppm": np.random.randint(0, 10, size=num_registros),
        "Calcio (Ca) ppm": np.random.randint(0, 1000, size=num_registros),
        "Cromo (Cr) ppm": np.random.randint(0, 10, size=num_registros),
        "Cobre (Cu) ppm": np.random.randint(0, 50, size=num_registros),
        "Hierro (Fe) ppm": np.random.randint(0, 300, size=num_registros),
        "Potasio (K) ppm": np.random.randint(0, 10, size=num_registros),
        "Magnesio (Mg) ppm": np.random.randint(0, 10, size=num_registros),
        "Molibdeno (Mo) ppm": np.random.randint(0, 10, size=num_registros),
        "Sodio (Na) ppm": np.random.randint(0, 30, size=num_registros),
        "Níquel (Ni) ppm": np.random.randint(0, 10, size=num_registros),
        "Plomo (Pb) ppm": np.random.randint(0, 10, size=num_registros),
        "Fósforo (P) ppm": np.random.randint(0, 10, size=num_registros),
        "Silicio (Si) ppm": np.random.randint(0, 50, size=num_registros),
        "Estaño (Sn) ppm": np.random.randint(0, 10, size=num_registros),
        "Titanio (Ti) ppm": np.random.randint(0, 10, size=num_registros),
        "Vanadio (V) ppm": np.random.randint(0, 10, size=num_registros),
        "Zinc (Zn) ppm": np.random.randint(0, 100, size=num_registros),
        "Residuo Ferroso Total mg/kg": np.random.randint(0, 600, size=num_registros),
        "Numero Muestra": [],
        "Numero Registro": [],
        "Numero Serie Equipo": []
    }

    # Generar números únicos
    for _ in range(num_registros):
        # Generar número de muestra
        letra_muestra = np.random.choice(list(NUM_MUESTRA_LETRAS))
        NUM_MUESTRA_DIGITOS += 1
        numero_muestra = f"{letra_muestra}{NUM_MUESTRA_DIGITOS:05d}"  # Formato: A00001, B00002, etc.

        # Generar número de registro
        NUM_REGISTRO += 1
        numero_registro = f"{NUM_REGISTRO:07d}"  # Formato: 0000001, 0000002, etc.

        # Generar número de serie del equipo
        numero_serie_equipo = f"LAJ{np.random.randint(0, 1000):03d}"  # Formato: LAJ001, LAJ999, etc.

        # Agregar los datos generados
        datos["Numero Muestra"].append(numero_muestra)
        datos["Numero Registro"].append(numero_registro)
        datos["Numero Serie Equipo"].append(numero_serie_equipo)

        # Asociar aceite lubricante al componente
        componente_seleccionado = datos["Componente"][-1]
        datos["Aceite Lubricante"].append(componentes_aceites.get(componente_seleccionado, "No especificado"))

    # Guardar el estado actualizado
    guardar_estado()

    # Convertir a DataFrame
    df = pd.DataFrame(datos)

    # Asignar criticidad controlada
    df["Criticidad"] = [generar_criticidad() for _ in range(num_registros)]

    # Ajustar valores según la criticidad asignada
    df = df.apply(ajustar_valores, axis=1)

    return df

# Función para guardar datos en el archivo CSV
def guardar_datos(df_nuevos, archivo="data/datos_generados.csv"):
    # Crear la carpeta 'data' si no existe
    os.makedirs(os.path.dirname(archivo), exist_ok=True)

    try:
        # Intentar leer el archivo existente
        df_existente = pd.read_csv(archivo)
        df_final = pd.concat([df_existente, df_nuevos], ignore_index=True)
    except FileNotFoundError:
        # Si el archivo no existe, usar solo los datos nuevos
        df_final = df_nuevos

    # Guardar el archivo actualizado
    df_final.to_csv(archivo, index=False)

# Bucle para generar datos cada 1 minuto
if __name__ == "__main__":
    while True:
        print("Generando 20 nuevos registros...")
        df_nuevos = generar_datos_aleatorios()
        guardar_datos(df_nuevos)
        print("Datos guardados. Esperando 1 minutos...\n")
        time.sleep(60)  # Esperar 1 minuto (60 segundos)