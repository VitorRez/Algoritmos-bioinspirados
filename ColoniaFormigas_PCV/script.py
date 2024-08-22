from ColoniaFormigas import *
import matplotlib.pyplot as plt

file = open("iteracoes1.txt", 'w')

iteracoes = []
resultados = []
rotas = []
melhor_caminho = 1000000

filename = "lau15_dist.txt"
for i in range(10000):
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

print(L)
plt.plot(iteracoes, resultados)
plt.xlabel('Iteração')
plt.ylabel('Distância')
plt.title('Convergência do Algoritmo')
plt.show()

