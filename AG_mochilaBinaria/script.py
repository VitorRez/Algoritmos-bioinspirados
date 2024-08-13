from AG import *
import csv

ng = 100
ni = 100


for i in range(5):
    valor_r = []
    peso_r = []
    for j in range(5):
        valor, peso = main(100, 50, ng, ni, 'p01', 0)
        valor_r.append(valor)
        peso_r.append(peso)
    with open("valor.csv", 'a') as csv_file:
        write_csv = csv.writer(csv_file)
        write_csv.writerow(valor_r)
    with open("peso.csv", 'a') as csv_file1:
        write_csv1 = csv.writer(csv_file1)
        write_csv1.writerow(peso_r)
    ng += 100
    ni += 100
            
