import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib
import time

def entrenar_modelo():
    # Paso 1: Cargar los datos
    try:
        df = pd.read_csv("data/datos_generados.csv")
        print("Datos cargados correctamente.")
    except FileNotFoundError:
        print("Error: El archivo 'data/datos_generados.csv' no existe.")
        return

    # Paso 2: Preprocesamiento
    # Eliminar columnas irrelevantes
    columnas_a_eliminar = [
        "Fecha",  # No es relevante para el modelo
        "nflota",  # Identificador no útil para la predicción
        "cambioLubricanate",  # Variable binaria que puede no ser relevante
        "Código ISO 4406",  # Código categórico sin relación directa con criticidad
        "Numero Muestra",  # Identificador único
        "Numero Registro",  # Identificador único
        "Numero Serie Equipo"  # Identificador único
    ]
    df = df.drop(columns=columnas_a_eliminar, errors="ignore")

    # Codificar variables categóricas
    df_encoded = pd.get_dummies(df, columns=["Equipo", "Componente", "Aceite Lubricante"])

    # Separar características (X) y etiquetas (y)
    X = df_encoded.drop(columns=["Criticidad"], errors="ignore")  # Variables independientes
    y = df_encoded["Criticidad"]  # Variable dependiente (objetivo)

    if X.empty or y.empty:
        print("Error: No hay suficientes datos para entrenar el modelo.")
        return

    # Dividir en entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Paso 3: Entrenar el modelo
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    # Evaluar el modelo
    y_pred = model.predict(X_test)
    print("\nReporte de Clasificación:")
    print(classification_report(y_test, y_pred))

    # Mostrar Importancia de Características
    print("\nImportancia de las Características:")
    feature_importances = pd.DataFrame({
        "Característica": X.columns,
        "Importancia": model.feature_importances_
    }).sort_values(by="Importancia", ascending=False)
    print(feature_importances)

    # Paso 4: Guardar el modelo entrenado
    joblib.dump(model, "data/modelo_entrenado.joblib")
    print("Modelo entrenado y guardado en 'data/modelo_entrenado.joblib'")

    # Guardar las características usadas para facilitar la integración con Streamlit
    joblib.dump(X.columns.tolist(), "data/feature_names.joblib")
    print("Nombres de características guardados en 'data/feature_names.joblib'")

# Bucle principal para ejecutar el entrenamiento cada 2 horas
if __name__ == "__main__":
    while True:
        print("\nIniciando proceso de entrenamiento...")
        entrenar_modelo()
        print("Esperando 2 horas antes del próximo entrenamiento...\n")
        time.sleep(7200)  # Esperar 2 horas (7200 segundos)