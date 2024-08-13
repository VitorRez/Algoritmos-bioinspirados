from AG import *
import matplotlib.pyplot as plt

e = [[500, 100, 100, 1], [500, 100, 80, 1],
     [500, 200, 80, 2], [500, 200, 70, 2],
     [500, 300, 70, 5], [500, 300, 70, 5]]

distancias = []
resultados = []
iteracoes = []

for params in e:
    distancia, resultado, iteracao = main(params[0], params[1], params[2], params[3], "AG_combinatorio/lau15_dist.txt")
    distancias.append(distancia)
    resultados.append(resultado)
    iteracoes.append(iteracao)

print(*distancias)

plt.figure(figsize=(10, 6))

for i in range(len(resultados)):
    plt.plot(iteracoes[i], resultados[i], label=f'Teste {i+1}')

plt.xlabel('Iteração')
plt.ylabel('Distância')
plt.title('Convergência do Algoritmo Genético')
plt.legend()
plt.show()
