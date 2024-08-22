import numpy as np
import copy
from random import randint, shuffle, random
import matplotlib.pyplot as plt

def get_cidades(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    tam = len(lines)
    matriz = [[int(j) for j in i.split()] for i in lines]

    return matriz, tam

def funcao_objetivo(rota, matriz_cidade, tam):
    dist = 0
    for i in range(tam-1):
        dist += matriz_cidade[rota[i]][rota[i+1]]
    dist += matriz_cidade[rota[tam-1]][rota[0]]
    return dist

def set_feromonio(tam, f):
    matriz = []
    for i in range(tam):
        aux = []
        for j in range(tam):
            if j != i:
                aux.append(f)
            else:
                aux.append(0)
        matriz.append(aux)
    return matriz

def atualiza_feromonio_AS(matriz_f, i, j, Q, L, m, p, aux):
    sum = 0
    if aux == True:
        for x in range(m):
            sum += Q/L
    matriz_f[i][j] = (1 - p)*matriz_f[i][j] + sum

def atualiza_feromonio_EAS(matriz_f, i, j, Q, L, m, p, aux1, aux2):
    sum = 0
    if aux1 == True and aux2 == True:
        for x in range(m):
            sum += Q/L + Q/L
    matriz_f[i][j] = (1 - p)*matriz_f[i][j] + sum

def funcao_probabilistica(matriz_c, matriz_f, i, j, k, a, b):
    sum = 0 
    for x in k:
        if x != i:
            sum += (matriz_f[i][x]**a)*((1/matriz_c[i][x])**b)
    return ((matriz_f[i][j]**a)*((1/matriz_c[i][j])**b))

def main(filename, num_iteracoes, Q, p, f, a, b, tipo):
    matriz_cidade, tam = get_cidades(filename)
    matriz_feromonio = set_feromonio(tam, f)
    
    ROTA = [x for x in range(tam)]
    shuffle(ROTA)
    L = funcao_objetivo(ROTA, matriz_cidade, tam)

    m = tam
    
    for iteracao in range(num_iteracoes):
        for formiga in range(m):
            s = [] #caminho atual
            sl = [x for x in range(tam)] #cidades disponiveis

            cidade = randint(0, tam-1)

            s.append(cidade)
            sl.remove(cidade)

            while len(s) < tam:
                melhor_probabilidade = 0
                prox_cidade = cidade + 1
                for j in sl:
                    if j != cidade:
                        probabilidade = funcao_probabilistica(matriz_cidade, matriz_feromonio, cidade, j, sl, a, b)

                        if probabilidade >= melhor_probabilidade:
                            melhor_probabilidade = probabilidade
                            prox_cidade = j
                s.append(prox_cidade)
                cidade = prox_cidade
                sl.remove(prox_cidade)

            distancia = funcao_objetivo(s, matriz_cidade, tam)

            if distancia < L:
                ROTA = copy.deepcopy(s)
                L = distancia

        if tipo == "AS":
            for i in range(tam-1):
                for x in range(tam-1):
                    if i == ROTA[x] and i+1 == ROTA[x+1]:
                        atualiza_feromonio_AS(matriz_feromonio, ROTA[i], ROTA[i+1], Q, L, m, p, True)
                    else:
                        atualiza_feromonio_AS(matriz_feromonio, ROTA[i], ROTA[i+1], Q, L, m, p, False)
        else:
            for i in range(tam-1):
                for x in range(tam-1):
                    if i == ROTA[x] and i+1 == ROTA[x+1]:
                        atualiza_feromonio_EAS(matriz_feromonio, ROTA[i], ROTA[i+1], Q, L, m, p, True, True)
                    else:
                        atualiza_feromonio_EAS(matriz_feromonio, ROTA[i], ROTA[i+1], Q, L, m, p, False, False)

    return ROTA, L

#ROTA, L = main(1, 100, 0.5, 10**-6, 1, 5, "AS")
#print(ROTA, L)