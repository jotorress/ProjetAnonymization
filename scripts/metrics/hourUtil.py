import csv
from Utils import separator  # Asegúrate de que separator es ',' para este caso

def main(nona, anon, parameters={}):
    total = 0
    filesize = 0
    hourdec = [1, 0.9, 0.8, 0.6, 0.4, 0.2, 0, 0.1, 0.2, 0.3, 0.4, 0.5,
               0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0, 0.2, 0.4, 0.6, 0.8, 0.9]

    with open(nona, "r") as fd_nona_file, open(anon, "r") as fd_anon_file:
        nona_reader = csv.reader(fd_nona_file, delimiter=separator)
        anon_reader = csv.reader(fd_anon_file, delimiter=separator)
        
        for row1, row2 in zip(nona_reader, anon_reader):
            score = 1
            filesize += 1
            if row2[0] == "DEL":
                continue
            
            # Asegúrate de que row2[1] tenga el formato esperado
            if len(row2[1]) > 13 and len(row2[0]):
                houranon = int(row2[1][11:13])
                hournona = int(row1[1][11:13])
                
                if 0 <= houranon < 24 and 0 <= hournona < 24:
                    if abs(houranon - hournona):  # Restar puntos por cada hora de diferencia
                        score -= hourdec[abs(houranon - hournona)]  # Resta basada en la diferencia de horas
                else:
                    print(f"Error: Hora fuera de rango en fila {filesize}.")
                    return (-1, filesize)
            else:
                print(f"Error: Formato incorrecto en fila {filesize}.")
                return (-1, filesize)

            total += max(0, score)
    
    return total / filesize if filesize > 0 else 0  # Evita división por cero
