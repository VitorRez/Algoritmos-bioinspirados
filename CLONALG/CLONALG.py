import random
import math
import copy
import matplotlib.pyplot as plt
import numpy as np

def get_cidades(arquivo):
    return np.loadtxt(arquivo, dtype=int)

def funcao_objetivo(ind, matriz):
    distancia = 0
    for i in range(len(ind) - 1):
        distancia += matriz[ind[i], ind[i + 1]]
    distancia += matriz[ind[-1], ind[0]]
    return 1 / distancia

def gerar_ind(tam):
    return np.random.permutation(tam)

def clonar(ind, adaptacao, fator, num_ind):
    num_replicas = int(round(fator * num_ind / (adaptacao + 1)))
    return [np.copy(ind) for _ in range(num_replicas)]

def mutacao(ind, p):
    if np.random.rand() < p:
        i, j = np.random.choice(len(ind), size=2, replace=False)
        ind[i], ind[j] = ind[j], ind[i]

def main(num_ind, num_ite, n, d, tc, filename):
    matriz = get_cidades(filename)
    tam = len(matriz)

    populacao = [gerar_ind(tam) for _ in range(num_ind)]
    adaptacoes = [funcao_objetivo(ind, matriz) for ind in populacao]

    melhor_solucao = None
    menor_valor = float('inf')
    h = []

    for iteracao in range(num_ite):
        melhores_indices = np.argsort(adaptacoes)[-n:]
        melhores_solucoes = [populacao[i] for i in melhores_indices]
        melhores_adaptacoes = [adaptacoes[i] for i in melhores_indices]

        clones = []
        for i in range(n):
            clones += clonar(melhores_solucoes[i], melhores_adaptacoes[i], tc, num_ind)

        for clone in clones:
            adaptacao = funcao_objetivo(clone, matriz)
            probabilidade_mutacao = np.exp(-adaptacao)
            mutacao(clone, probabilidade_mutacao)

        adaptacoes_clones = [funcao_objetivo(clone, matriz) for clone in clones]

        melhores_clones_indices = np.argsort(adaptacoes_clones)[-n:]
        populacao = [clones[i] for i in melhores_clones_indices]
        adaptacoes = [adaptacoes_clones[i] for i in melhores_clones_indices]

        for _ in range(d):
            nova_solucao = gerar_ind(tam)
            populacao.append(nova_solucao)
            adaptacoes.append(funcao_objetivo(nova_solucao, matriz))

        indice_melhor = np.argmax(adaptacoes)
        melhor_atual = populacao[indice_melhor]
        menor_atual = 1 / adaptacoes[indice_melhor]

        if menor_atual < menor_valor:
            melhor_solucao = melhor_atual
            menor_valor = menor_atual

        h.append(menor_valor)

    return melhor_solucao, menor_valor, h

def exibir_grafico(evolucao):
    plt.plot(evolucao)
    plt.xlabel('Iterações')
    plt.ylabel('Melhor Valor Encontrado')
    plt.title('Evolução do Melhor Valor')
    plt.show()

m, d, h = main(20, 150, 10, 5, 2, 'CLONALG/lau15_dist.txt')

print(m, d)

exibir_grafico(h)
