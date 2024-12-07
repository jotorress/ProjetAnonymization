import csv
import pandas as pd # type: ignore
import numpy as np # type: ignore
import os
import zipfile

separator = ","

#################################
#       Global functions        #
#################################

def csv_length(filename):
    try:
        return sum(1 for line in open(filename))
    except:
        return -1

def csv_width(filename):
    return sum(1 for char in next(open(filename)) if char == separator) + 1

def del_indexes(filename):
    index = 0
    indexes = []
    fd = open(filename, "r")
    nona_reader = csv.reader(fd, delimiter=separator)
    for row in nona_reader:
        if row[0] == "DEL":
            indexes += [index]
        index += 1
    return indexes

def checking_shape(input, default):
    length = 0
    size = (csv_length(default), csv_width(default))
    if size[0] < 0 or size[1] < 0:
        return (-1, 0)  # If the original file has a correct shape
    # Checking the number of rows and columns
    try:
        for line in open(input):
            if line[0:3] != "DEL" and sum(1 for char in line if char == separator) + 1 != size[1]:
                return (-2, length)
            length += 1
    except:
        return (-3, 0)
    return (-4, length) if length != size[0] else (1, 0)

# Shuffling a chunk
def chunk_shuffler(filename, offset, toRead):
    df = pd.read_csv(filename, skiprows=offset, nrows=toRead, header=None, dtype=object, sep=separator)
    return df.reindex(np.random.permutation(df.index))

def unzip_file(filename):
    filenamezip = filename + ".zip"
    directoryname = filename + "_directory"
    
    with zipfile.ZipFile(filenamezip, 'r') as zip_ref:
        # Raise if the file is bigger than 10Go
        if zip_ref.infolist()[0].file_size > 10000000000:
            raise SystemExit('File to unzip too big (BombZip?)')
        zip_ref.extract(zip_ref.infolist()[0], path=directoryname)
    os.rename(directoryname + "/" + zip_ref.infolist()[0].filename, filename)
    os.rmdir(directoryname)

def zip_outfileShuffle(filename):
    filenamezip = filename + ".zip"
    with zipfile.ZipFile(filenamezip, 'w', compression=zipfile.ZIP_DEFLATED) as zip_ref:
        zip_ref.write(filename)

def error_messages(errortuple):
    if errortuple[0] == -1:
        return "le fichier original est invalide"
    elif errortuple[0] == -2:
        return "le fichier déposé est invalide (mauvais nombre de colonnes)\n ligne " + str(errortuple[1])
    elif errortuple[0] == -3:
        return "le fichier déposé est invalide\n (mauvais format)"
    elif errortuple[0] == -4:
        return "le fichier déposé est invalide (mauvais nombre de lignes)"
    elif errortuple[0] == -5:
        return "un utilisateur posséde plusieurs identifiants par semaine\n ligne " + str(errortuple[1])
    elif errortuple[0] == -6:
        return "un identifiant est manquant\n ligne "+str(errortuple[1])
    elif errortuple[0] == -7:
        return "erreur dans le calcul d’utilité (Vérifiez votre fichier déposé)\n ligne " + str(errortuple[1])
    elif errortuple[0] == -8:
        return "erreur dans le script " + errortuple[1]
    elif errortuple[0] == -9:
        return "aucun script d'utilité fonctionnel trouvé"
    elif errortuple[0] == -10:
        return "La date est inexistante ou mal formatée\n ligne " + str(errortuple[1])
    elif errortuple[0] == -11:
        return "Le fichier ZIP est mal formatté"
    elif errortuple[0] == -12:
        return "Erreur fichier ZIP Administrateur"

# Custom default dict
def list_struct():
    return [float(), float()]

def main(nona, anon, parameters={}):
    total = 0
    filesize = 0
    # Set the amount linked to the hour gap
    hourdec = [1, 0.9, 0.8, 0.6, 0.4, 0.2, 0, 0.1, 0.2, 0.3, 0.4, 0.5,
               0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0, 0.2, 0.4, 0.6, 0.8, 0.9]
    fd_nona_file = open(nona, "r")
    fd_anon_file = open(anon, "r")
    nona_reader = csv.reader(fd_nona_file, delimiter=separator)
    anon_reader = csv.reader(fd_anon_file, delimiter=separator)
    
    for row1, row2 in zip(nona_reader, anon_reader):
        score = 1
        filesize += 1
        if row2[0] == "DEL":
            continue
        if len(row2[1]) > 19:  # Verificando la longitud del timestamp "YYYY-MM-DD HH:MM:SS"
            houranon = int(row2[1][11:13])  # Obtener la hora de la posición anonimizada
            hournona = int(row1[1][11:13])   # Obtener la hora de la posición no anonimizada
            if 0 <= houranon < 24 and 0 <= hournona < 24:
                if abs(houranon - hournona):  # Subtract 0,1 points per hour
                    score -= hourdec[abs(houranon - hournona)]  # Subtract the amount linked to the hour gap
            else:
                return (-1, filesize)
        else:
            return (-1, filesize)
        total += max(0, score) if row2[0] != "DEL" else 0
    
    return total / filesize
