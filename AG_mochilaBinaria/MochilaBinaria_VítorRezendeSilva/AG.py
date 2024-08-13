import numpy
import random
from random import randint
import matplotlib.pyplot as plt


def cria_pop(num_individuos, tam):
    pop = []
    for i in range(num_individuos):
        ind = []
        for j in range(tam):
            ind.append(randint(0,1))
        pop.append(ind)
    return pop

def cruzamento(p1, p2, tam, tc):
    t = randint(0, 100)
    if(t > tc):
        return p1, p2
    f1 = []
    f2 = []
    ponto = randint(1, tam-2)
    for i in range(0, ponto):
        f1.append(p1[i])
        f2.append(p2[i])
    for i in range(ponto, tam):
        f1.append(p2[i])
        f2.append(p1[i])
    return f1, f2


def roleta(pop, num_individuos, capacity, weight_list, profit_list):
    cont = 0
    melhores = []
    roleta = []
    total = 0
    for i in pop:
        total += funcao_objetivo(i, capacity, weight_list, profit_list)
    for j in pop:
        roleta.append(funcao_objetivo(j, capacity, weight_list, profit_list)/total)
    while cont < num_individuos:
        r = random.uniform(0, 1)
        x = 0
        i = 0
        while x < r:
            x += roleta[i]
            i += 14
        melhores.append(pop[i-1])
        cont += 1

    return melhores

def torneio(pop, num_individuos, capacity, weight_list, profit_list):
    cont = 0
    melhores = []
    while cont < num_individuos:
        ind1 = randint(0, num_individuos-1)
        ind2 = randint(0, num_individuos-1)
        while ind1 == ind2:
            ind2 = randint(0, num_individuos-1)
        resul1 = funcao_objetivo(pop[ind1], capacity, weight_list, profit_list)
        resul2 = funcao_objetivo(pop[ind2], capacity, weight_list, profit_list)
        if resul1 < resul2:
            melhores.append(pop[ind1])
        else:
            melhores.append(pop[ind2])
        cont += 1
    return melhores

def mutacao(ind, tm):
    for i in ind:
        x = randint(0, 100)
        if x <= tm:
            i = randint(0, 1)

def nova_pop(pop, tam, tm, tc, num_filhos, melhor):
    pop_filhos = []
    cont = 0
    pop_filhos.append(melhor)
    while len(pop_filhos) <= len(pop):
        p1 = randint(0, num_filhos-1)
        p2 = randint(0, num_filhos-1)
        while p2 == p1:
            p2 = randint(0, num_filhos-1)
        f1, f2 = cruzamento(pop[p1], pop[p2], tam, tc)
        pop_filhos.append(f1)
        pop_filhos.append(f2)
    pop_filhos.pop(len(pop_filhos)-1)

    cont = 0
    for i in pop_filhos:
        if cont != 0:
            mutacao(i, tm)
        cont += 1

    return pop_filhos

def calc_peso(ind, weight_list):
    weight = 0
    for index, i in enumerate(weight_list):
        if ind[index] == 1:
            weight += i
    return weight

def melhor_ind(pop, capacity, weight_list, profit_list):
    melhor = funcao_objetivo(pop[0], capacity, weight_list, profit_list)
    indice_melhor = 0
    for i in pop:
        x = funcao_objetivo(i, capacity, weight_list, profit_list)
        w = calc_peso(i, weight_list)
        if x >= melhor and w <= capacity:
            melhor = x
            indice_melhor = pop.index(i)
    return indice_melhor

def funcao_objetivo(ind, capacity, weight_list, profit_list):
    profit = 0
    weight = 0
    for index, i in enumerate(profit_list):
        if ind[index] == 1:
            profit += i
    for index, j in enumerate(weight_list):
        if ind[index] == 1:
            weight += j
    if weight <= capacity:
        return profit
    else:
        return profit * (1-(weight-capacity)/capacity)
    
def main(tc, tm, n, num_individuos, filename):
    file_c = open(filename + "_c.txt", 'r')
    file_w = open(filename + "_w.txt", 'r')
    file_p = open(filename + "_p.txt", 'r')
    file1 = open("gen.txt", 'w')

    weight_list = []
    profit_list = []

    capacity = int(file_c.readline())
    for i in file_w.readlines():
        weight_list.append(int(i))
    for j in file_p.readlines():
        profit_list.append(int(j))
    tam = len(profit_list)

    file_c.close()
    file_w.close()
    file_p.close()

    print(capacity)
    print(weight_list)
    print(profit_list)
    print(tam)

    resultados = []
    iteracao = []
    parada = 0

    pop = cria_pop(num_individuos, tam)

    while parada < n:
        indice = melhor_ind(pop, capacity, weight_list, profit_list)
        melhor = pop[indice]

        file1.write(str(pop[indice]) + "\n")
        file1.write(str(funcao_objetivo(pop[indice], capacity, weight_list, profit_list)))
        file1.write("\n------------------------------------------------------\n")
        
        resultados.append(funcao_objetivo(pop[indice], capacity, weight_list, profit_list))
        iteracao.append(parada)

        pop = torneio(pop, num_individuos, capacity, weight_list, profit_list)

        pop = nova_pop(pop, tam, tm, tc, num_individuos, melhor)
        parada += 1 

    print("Resultado: " + str(pop[indice]))
    print("Valor (fitness) do melhor indivíduo: " + str(funcao_objetivo(pop[indice], capacity, weight_list, profit_list)))
    print("Peso do melhor indivíduo: " + str(calc_peso(pop[indice], weight_list)))
    print("Média dos fitness: " + str(sum(resultados)/n))
    file1.write("\n------------------------------------------------------\n")

    file1.write("Media dos fitness: " + str(sum(resultados)/n) + "\n")
    file1.close()



    plt.plot(iteracao, resultados)
    plt.show()

    return funcao_objetivo(pop[indice], capacity, weight_list, profit_list), calc_peso(pop[indice], weight_list)

