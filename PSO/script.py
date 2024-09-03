from PSO import Enxame, Particula
import matplotlib.pyplot as plt

file = open("iteracoes.txt", 'w')

iteracoes = []
resultados = []
rotas = []
melhor = 1000000
cont = 0

for i in range(1000):
    print(i)
    E = Enxame(-2.0, 2.0, -1.0, 1.0, 1.5, 2.0, 100, 100, 2, 0.7)
    gbest, gbestf = E.PSO()
    file.write(str(gbestf) + " " + str(gbest) + "\n")
    iteracoes.append(i)
    resultados.append(gbestf)
    if gbestf < melhor:
        melhor = gbestf
        cont += 1

print(f"Melhor resultado encontrado: {melhor}\nVezes que um valor menor foi encontrado: {cont}")
plt.plot(iteracoes, resultados)
plt.xlabel('Iteração')
plt.ylabel('Fitness')
plt.show()