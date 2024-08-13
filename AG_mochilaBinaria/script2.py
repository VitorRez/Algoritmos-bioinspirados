from AG import *
import csv
import matplotlib.pyplot as plt

valores = []
pesos = []
iteracoes = []

for i in range(10):
    valor, peso = main(100, 50, 400, 400, 'p01', 0)
    valores.append(valor)
    pesos.append(peso)
    iteracoes.append(i)

    with open("resultados.csv", 'a') as csv_file:
        write_csv = csv.writer(csv_file)
        write_csv.writerow([valor, peso])

plt.plot(iteracoes, valores, label = "valores")
plt.plot(iteracoes, pesos, label = "pesos")
plt.legend()
plt.show()
