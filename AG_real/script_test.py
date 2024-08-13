import AG
import csv

tm = [1, 5, 10]
tc = [50, 80, 100]
num_individuos = [25, 50, 100]
n = [25, 50, 100]
cruzamento = ["BLXa", "BLXab"]

for i in tc:
    for j in tm:
        for k in n:
            for l in num_individuos:
                for m in cruzamento:
                    fitness, media = AG.AG_real(i, j, k, l, m, 0)

                    with open("resultados.csv", "a") as file2:
                        csv_writer = csv.writer(file2)
                        csv_writer.writerow([i, j, k, l, m, fitness, media])