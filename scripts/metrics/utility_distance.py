import csv
import sys
from Utils import separator  # Définir votre propre séparateur Ex: '\t', ' '

#################################
#         Global variables      #
# To know:                      #
# dx =1 means that you allow    #
# a maximum of 111.195km        #
# 0.0001 : cellule au mètre     #
# 0.001 : cellule à la rue      #
# 0.01 : cellule au quartier    #
# 0.1 : cellule à la ville      #
# 1 : cellule à la région       #
# 10 : cellule au pays          #
#                               #
#################################
dx = 0.1

#################################
#         Function              #
#################################
def calcul_utility(diff):
    score = diff * (-1 / dx) + 1
    if score < 0:
        return 0
    return score

#################################
#         Utility Function      #
#################################
def main(fd_anon_file, fd_nona_file, parameters={"dx": 0.1}):
    global dx
    dx = parameters.get('dx', 0.1)  # Obtener 'dx' de los parámetros, o usar 0.1 por defecto
    utility = 0
    line_utility = 0
    filesize = 0

    try:
        with open(fd_nona_file, "r") as fd_nona:
            nona_reader = csv.reader(fd_nona, delimiter=separator)
            with open(fd_anon_file, "r") as fd_anon:
                anon_reader = csv.reader(fd_anon, delimiter=separator)

                # Leer los archivos y calcular
                for lineAno, lineNonAno in zip(nona_reader, anon_reader):
                    if lineAno[0] != "DEL":
                        try:
                            diff_lat = abs(float(lineNonAno[3]) - float(lineAno[3]))
                            diff_long = abs(float(lineNonAno[2]) - float(lineAno[2]))
                            diff = diff_lat + diff_long
                            line_utility += calcul_utility(diff)
                            filesize += 1  # Incrementar filesize aquí solo si se calculó la utilidad
                        except (ValueError, IndexError) as e:
                            print(f"Error procesando líneas: {lineAno}, {lineNonAno}. Error: {e}")
                    else:
                        # Si la línea contiene "DEL", no sumamos utilidad, pero contamos la línea
                        filesize += 1

                if filesize > 0:
                    utility = line_utility / filesize
                else:
                    print("No se procesaron líneas válidas.")
                    return 0  # Devolver 0 o un valor por defecto si no se procesaron líneas

    except FileNotFoundError as e:
        print(f"Error: {e}. Verifique que el archivo exista.")
        sys.exit(1)
    except Exception as e:
        print(f"Error inesperado: {e}")
        sys.exit(1)

    return utility
