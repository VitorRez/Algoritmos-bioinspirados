from ColoniaFormigas import *
import matplotlib.pyplot as plt

file = open("iteracoes2.txt", 'w')

iteracoes = []
resultados = []
rotas = []
melhor_caminho = 1000000
cont = 0

filename = "sgb128_dist.txt"
for i in range(100):
    print(i)
    if i % 2 == 0:
        S, L = main(filename, 1, 100, 0.5, 10**-6, 1, 5, "AS")
    else:
        S, L = main(filename, 1, 100, 0.5, 10**-6, 1, 5, "EAS")
    file.write(str(L) + " " +str([S]) + "\n")
    iteracoes.append(i)
    resultados.append(L)
    if L < melhor_caminho:
        melhor_caminho = L
        cont += 1

print(L)
print(melhor_caminho)
print(cont)
plt.plot(iteracoes, resultados)
plt.xlabel('Iteração')
plt.ylabel('Distância')
plt.title('Convergência do Algoritmo Genético')
plt.show()

