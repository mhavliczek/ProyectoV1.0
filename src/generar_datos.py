import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import os

# Parámetros
num_registros = 20  # Número de registros a generar cada vez
equipos = ["CATERPILLAR 797F", "CATERPILLAR 988H", "CATERPILLAR 24M"]
componentes = ["MANDO FINAL", "TRANSMISIÓN", "DIFERENCIAL"]

# Función para generar datos aleatorios
def generar_datos_aleatorios():
    datos = {
        "Fecha": [datetime.now() + timedelta(minutes=5 * i) for i in range(num_registros)],
        "Equipo": np.random.choice(equipos, size=num_registros),
        "Componente": np.random.choice(componentes, size=num_registros),
        "Hierro (ppm)": np.random.randint(0, 500, size=num_registros),
        "Silicio (ppm)": np.random.randint(0, 25, size=num_registros),
        "Residuo Ferroso (mg/kg)": np.random.randint(0, 500, size=num_registros),
        "Viscosidad": np.random.uniform(40, 60, size=num_registros),  # Viscosidad simulada
    }
    return pd.DataFrame(datos)

# Función para guardar datos en el archivo CSV
def guardar_datos(df_nuevos, archivo="data/datos_generados.csv"):
    # Crear la carpeta 'data' si no existe
    os.makedirs(os.path.dirname(archivo), exist_ok=True)

    try:
        # Leer el archivo existente
        df_existente = pd.read_csv(archivo)
        # Concatenar los datos nuevos con los existentes
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
        print("Datos guardados. Esperando 1 minuto...\n")
        time.sleep(60)  # Esperar 1 minuto (60 segundos)