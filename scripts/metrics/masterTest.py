import pandas as pd

def main(originalFile, anonymisedFile):
    """
    Este script compara el número de filas entre el archivo original y el archivo anonimizado.

    Parámetros:
    originalFile: Ruta al archivo de datos original (CSV).
    anonymisedFile: Ruta al archivo de datos anonimizados (CSV).

    Retorna:
    Un puntaje de utilidad basado en la similitud del número de filas (1 si es idéntico, 0 si es completamente diferente).
    """
    try:
        # Leer los archivos originales y anonimizados
        original_data = pd.read_csv(originalFile)
        anonymised_data = pd.read_csv(anonymisedFile)

        # Contar el número de filas
        original_rows = len(original_data)
        anonymised_rows = len(anonymised_data)

        # Calcular el puntaje (1 si son iguales, 0 si hay una gran diferencia)
        if original_rows == anonymised_rows:
            score = 1  # Máxima utilidad si las filas coinciden
        else:
            # Penalización proporcional a la diferencia en filas
            score = max(0, 1 - abs(original_rows - anonymised_rows) / original_rows)

        return score

    except Exception as e:
        # En caso de error, imprimirlo y devolver un puntaje de 0
        print(f"Error al procesar los archivos: {e}")
        return 0

if __name__ == "__main__":
    # Define las rutas de los archivos
    original_file = "ruta/al/archivo_original.csv"
    anonymised_file = "ruta/al/archivo_anonimizado.csv"

    # Llama a la función main y muestra el resultado
    utility_score = main(original_file, anonymised_file)
    print(f"Puntaje de utilidad: {utility_score}")
