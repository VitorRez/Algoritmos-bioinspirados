import AG
import csv

entradas = [[80, 1, 100, 100, 1, 0], [80, 5, 50, 100, 1, 0], 
            [80, 5, 100, 100, 1, 0], [80, 10, 100, 100, 1, 0],
            [100, 1, 50, 100, 1, 0], [100, 1, 50, 100, 0, 0],
            [100, 1, 100, 100, 1, 0], [100, 5, 50, 100, 1, 0],
            [100, 5, 100, 100, 0, 0], [100, 5, 100, 100, 1, 0],
            [100, 10, 100, 100, 0, 0], [100, 10, 100, 100, 1, 0]]


with open("resultados2.csv", "a") as file2:
    for i in entradas:
        for x in range(10):
            if i[4] == 0:
                y = 'BLXa'
            else:
                y = 'BLXab'
    
            fitness, media = AG.AG_real(i[0], i[1], i[2], i[3], y, i[5])
            
            
            csv_writer = csv.writer(file2)
            csv_writer.writerow([x, i[0], i[1], i[2], i[3], y, fitness, media])