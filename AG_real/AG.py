import numpy
import random
from random import randint
import matplotlib.pyplot as plt

#cria uma população de individuos usando o num de individuos e o seu tamanho como parametro
def cria_pop(num_individuos, tam):
    pop = []
    for i in range(num_individuos):
        ind = []
        for j in range(tam):
            ind.append(random.uniform(-2,2))
        pop.append(ind)
    return pop


def cruzamento_BLXa(p1, p2, tam, a, tc):
    t = randint(0, 100)
    if(t > tc):
        return p1, p2
    d = []
    f1 = []
    f2 = []
    i = 0
    while i < tam:
        d.append(abs(p1[i]-p2[i]))
        u = random.uniform(min(p1[i], p2[i])-a*d[i], max(p1[i], p2[i])+a*d[i])
        f1.append(u)
        u = random.uniform(min(p1[i], p2[i])-a*d[i], max(p1[i], p2[i])+a*d[i])
        f2.append(u)
        i += 1
    return f1, f2

def cruzamento_BLXab(p1, p2, tam, a, b, tc):
    t = randint(0, 100)
    if(t > tc):
        return p1, p2
    if funcao_objetivo(p1) < funcao_objetivo(p2):
        X = p1
        Y = p2
    else:
        X = p2
        Y = p1
    f1 = []
    f2 = []
    d = []
    i = 0
    while i < tam:
        d.append(abs(X[i] - Y[i]))
        if(X[i] <= Y[i]):
            u = random.uniform(X[i] - a*d[i], Y[i] + b*d[i])
            f1.append(u)
            u = random.uniform(X[i] - a*d[i], Y[i] + b*d[i])
            f2.append(u)
        else:
            u = random.uniform(Y[i] - b*d[i], X[i] + a*d[i])
            f1.append(u)
            u = random.uniform(Y[i] - b*d[i], X[i] + a*d[i])
            f2.append(u)
        i += 1
    return f1, f2

#realiza a seleção de pais a partir de uma roleta
def roleta(pop, num_individuos):
    cont = 0
    melhores = []
    roleta = []
    total = 0
    for i in pop:
        total += 1/funcao_objetivo(i)
    for j in pop:
        roleta.append((1/funcao_objetivo(j))/total)
    while cont < num_individuos:
        r = random.uniform(0, 1)
        x = 0
        i = 0
        while x < r:
            x += roleta[i]
            i += 1
        melhores.append(pop[i-1])
        cont += 1
    return melhores

#realiza a mutação de individuos, pra cada valor individual é sorteado um valor de 0 a 100, se ele
#for menor que a taxa de mutação seu valor é trocado
def mutacao(ind, tm):
    for i in ind:
        x = randint(0, 100)
        if x <= tm:
            i = random.uniform(-2, 2)

#cria uma nova população, com individuos gerados por cruzamento através dos vencedores do torneio
#e o melhor individuo da população interior
def nova_pop(pop, tam, tm, tc, num_filhos, melhor, cruzamento):
    pop_filhos = []
    cont = 0
    pop_filhos.append(melhor)
    while len(pop_filhos) <= num_filhos:
        p1 = randint(0, num_filhos-1)
        p2 = randint(0, num_filhos-1)
        while p2 == p1:
            p2 = randint(0, num_filhos-1)
        if cruzamento == "BLXa":
            f1, f2 = cruzamento_BLXa(pop[p1], pop[p2], tam, 0.75, tc)
        else:
            f1, f2 = cruzamento_BLXab(pop[p1], pop[p2], tam, 0.75, 0.25, tc)
        pop_filhos.append(f1)
        pop_filhos.append(f2)
    pop_filhos.pop(len(pop_filhos)-1)
    
    cont = 0
    for i in pop_filhos:
        if cont != 0:
            mutacao(i, tm)
        cont += 1

    return pop_filhos

#função objetivo
def funcao_objetivo(ind):
    x1 = ind[0]
    x2 = ind[1]
    x3 = ind[2]

    return (-20 * pow(numpy.e, (-0.2 * numpy.sqrt((1 / 3) * (x1**2+x2**2+x3**2))))) - (pow(numpy.e, ((1 / 3) * (numpy.cos(2*numpy.pi*x1)+ numpy.cos(2*numpy.pi*x2) + numpy.cos(2*numpy.pi*x3))))) + 20 + numpy.e


#retorna o melhor individuo de uma população
def melhor_ind(pop):
    melhor = funcao_objetivo(pop[0])
    indice_melhor = 0
    for i in pop:
        x = funcao_objetivo(i)
        if x < melhor:
            melhor = x
            indice_melhor = pop.index(i)
    return indice_melhor

def AG_real(tc, tm, n, num_individuos, cruzamento, plot):
    tam = 3
    resultados = []
    iteracao = []
    parada = 0
    file1 = open("gen.txt", "w")

    pop = cria_pop(num_individuos, tam)

    while parada < n:
        indice = melhor_ind(pop)
        melhor = pop[indice]

        file1.write(str(pop[indice]) + "\n")
        file1.write(str(funcao_objetivo(pop[indice])))
        file1.write("\n------------------------------------------------------\n")
        
        resultados.append(funcao_objetivo(pop[indice]))
        iteracao.append(parada)

        pop = roleta(pop, num_individuos)

        pop = nova_pop(pop, tam, tm, tc, num_individuos, melhor, cruzamento)
        parada += 1 

    print("Resultado: " + str(pop[indice]))
    print("Fitness do melhor indivíduo: " + str(funcao_objetivo(pop[indice])))
    print("Média dos fitness: " + str(sum(resultados)/n))
    file1.write("\n------------------------------------------------------\n")

    file1.write("Media dos fitness: " + str(sum(resultados)/n) + "\n")
    file1.close()

    if plot == 1:
        plt.plot(iteracao, resultados)
        plt.show()

    return funcao_objetivo(pop[indice]), sum(resultados)/n