import numpy 
import copy
from random import randint, shuffle, random
import matplotlib.pyplot as plt

def cria_pop(num_individuos, tam):
    pop = []
    for i in range(num_individuos):
        ind = [j for j in range(tam)]
        shuffle(ind)
        pop.append(ind)
    return pop

def funcao_objetivo(ind, matriz):
    dist = 0
    tam = len(ind)
    for i in range(tam-1):
        dist += matriz[ind[i]][ind[i+1]]
    dist += matriz[ind[tam-1]][ind[0]]
    return dist

def melhor_ind(pop, matriz):
    tam = len(pop)
    melhor = funcao_objetivo(pop[0], matriz)
    indice = 0
    
    for i in range(1, tam-1):
        x = funcao_objetivo(pop[i], matriz)
        if x <= melhor:
            melhor = x
            indice = i
    return indice, melhor

def cruzamento(p1, p2, tc):
    if random() > tc/100:
        return p1, p2
    
    tam = len(p1)

    f1 = ['x' for i in range(tam)]
    f2 = ['x' for i in range(tam)]

    f1_aux = []
    f2_aux = []

    x1 = randint(0, tam)
    x2 = randint(0, tam)
    while(x1 == x2):
        x2 = randint(0, tam)

    if x1 > x2:
        mx = x1
        mn = x2
    else:
        mx = x2
        mn = x1

    for i in range(mx, tam):
        f1_aux.append(p2[i])
        f2_aux.append(p1[i])

    for i in range(mn, mx):
        f1[i] = p2[i]
        f2[i] = p1[i]
        f1_aux.append('x')
        f2_aux.append('x')

    for i in range(0, mn):
        f1_aux.append(p2[i])
        f2_aux.append(p1[i])

    j = 0
    for i in range(tam):
        if f1[i] == 'x':
            while f1_aux[j] == 'x':
                j += 1
            f1[i] = f1_aux[j]
            f2[i] = f2_aux[j]
            j += 1
        
    return f1, f2

def torneio(pop, num_individuos, matriz):
    tam = len(pop[0])
    melhores = []
    i = 0

    while len(melhores) < num_individuos:
        p1 = randint(0, tam-1)
        p2 = randint(0, tam-1)
        while p1 == p2:
            p2 = randint(0, tam-1)

        dist1 = funcao_objetivo(pop[p1], matriz)
        dist2 = funcao_objetivo(pop[p2], matriz)

        if dist1 <= dist2:
            melhores.append(pop[p1])
        else:
            melhores.append(pop[p2])
    
    return melhores

def mutacao(ind, tm):
    tam = len(ind)
    for i in range(tam):
        if random() <= tm / 100:
            j = randint(0, tam-1)
            ind[i], ind[j] = ind[j], ind[i]

def nova_pop(pop, tc, tm, num_individuos, melhor):
    tam = len(pop[0])

    pop_filhos = [copy.deepcopy(melhor)]


    i = 0
    while len(pop_filhos) < num_individuos:
        if i+1 >= tam:
            break

        f1, f2 = cruzamento(pop[i], pop[i+1], tc)
        pop_filhos.append(f1)
        if len(pop_filhos) < num_individuos:
            pop_filhos.append(f2)

    for i in range(1, num_individuos):
        mutacao(pop_filhos[i], tm)

    return pop_filhos

def get_cidades(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    tam = len(lines)
    matriz = [[int(j) for j in i.split()] for i in lines]

    return matriz, tam

def main(num_iteracoes, num_individuos, tc, tm, filename):
    file = open("AG_combinatorio/gen.txt", "w")
    matriz, tam = get_cidades(filename)
    cont = 0
    iteracao = []
    resultados = []

    pop = cria_pop(num_individuos, tam)

    indice, distancia = melhor_ind(pop, matriz)
    melhor = copy.deepcopy(pop[indice])

    while cont < num_iteracoes:

        file.write(str(pop[indice]) + "\n")
        file.write(str(distancia) + " " + str(cont))
        file.write("\n--------------------------------------------------------\n")

        resultados.append(distancia)
        iteracao.append(cont)

        melhores = torneio(pop, num_individuos, matriz)
        pop = nova_pop(melhores, tc, tm, num_individuos, melhor)

        indice, distancia = melhor_ind(pop, matriz)
        melhor = copy.deepcopy(pop[indice])

        cont += 1

    print(str(cont))
    print(str(melhor))
    print(str(distancia))

    file.write(str(melhor) + "\n")
    file.write(str(distancia))
    file.write("\n--------------------------------------------------------\n")
    file.close()

    plt.plot(iteracao, resultados)
    plt.xlabel('Iteração')
    plt.ylabel('Distância')
    plt.title('Convergência do Algoritmo Genético')
    plt.show()

    return distancia, resultados, iteracao