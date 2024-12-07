import random
from threading import Thread
from Utils import *  # Asegúrate de que esta importación sea correcta y que Utils tenga las funciones necesarias

#################################
#         Thread class          #
#################################

# Shuffling the submitted file for attackers
class Shuffle(Thread):
    def __init__(self, input, origin, output, dbconn):
        Thread.__init__(self)
        self.input = input
        self.origin = origin
        self.output = output
        self.dbconn = dbconn
        self.chunksize = 10000000

    def run(self):
        size = csv_length(self.origin)  # Asegúrate de que esta función esté definida en Utils
        chunks = 0  # Total number of chunks
        tmp = size
        while tmp > 0:
            tmp -= self.chunksize
            chunks += 1
        random_order = [i for i in range(chunks)]  # Posición del chunk en el archivo mezclado
        random.shuffle(random_order)
        
        for i in random_order:
            rows2read = self.chunksize if self.chunksize * (i + 1) < size else size - self.chunksize * i
            # Mezcla y añade el resultado CSV en el archivo dado
            chunk_shuffler(self.input, self.chunksize * i, rows2read).to_csv(self.output, mode="a", sep=separator,
                                                                             index=False, header=None)

        # Actualiza la base de datos
        self.dbconn.cursor().execute(f"UPDATE anonymisation \
                              SET status='Génération du fichier mélangé terminée' \
                              WHERE fileLink='{self.input.split('/')[1]}'")
        self.dbconn.commit()
