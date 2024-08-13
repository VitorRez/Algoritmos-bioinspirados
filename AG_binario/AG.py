import numpy
import math
import random
from random import randint
import matplotlib.pyplot as plt

#cria uma população de individuos usando o num de individuos e o seu tamanho como parametro
def cria_pop(num_individuos, tam):
    pop = []
    for i in range(num_individuos):
        ind = []
        for j in range(tam):
            ind.append(random.randint(0,1))
        pop.append(ind)
    return pop

#realiza o cruzamento entre 2 indivíduos em 1 ponto
def cruzamento(p1, p2, tam):
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

#realiza o torneio entre os indivíduos, isso é feito criando uma lista de mesmo tamanho da população
#a cada iteração, dois indivíduos aleatórios são selecionados e comparados, o melhor entre eles 
#vai compor a lista dos melhores, isso é feito até que essa lista tenha o mesmo tamanho da população
def torneio(pop, num_individuos):
    cont = 0
    melhores = []
    while cont < num_individuos:
        ind1 = randint(0, num_individuos-1)
        ind2 = randint(0, num_individuos-1)
        while ind1 == ind2:
            ind2 = randint(0, num_individuos-1)
        resul1 = funcao_objetivo(pop[ind1])
        resul2 = funcao_objetivo(pop[ind2])
        if resul1 <= resul2:
            melhores.append(pop[ind1])
        else:
            melhores.append(pop[ind2])
        cont += 1
    return melhores

#realiza a mutação de individuos, pra cada valor individual é sorteado um valor de 0 a 100, se ele
#for menor que a taxa de mutação seu valor é trocado
def mutacao(ind, tm):
    for i in ind:
        x = randint(0, 100)
        if x <= tm:
            if i == 0:
                i = 1
            else:
                i = 0

#cria uma nova população, com individuos gerados por cruzamento através dos vencedores do torneio
#e o melhor individuo da população interior
def nova_pop(pop, tam, tm, num_filhos, melhor):
    pop_filhos = []
    cont = 0
    i = 0
    pop_filhos.append(melhor)
    while i < num_filhos - 1:
        f1, f2 = cruzamento(pop[i], pop[i+1], tam)
        pop_filhos.append(f1)
        pop_filhos.append(f2)
        i+=1
        cont+=1
    
    cont = 0
    for i in pop_filhos:
        if cont != 0:
            mutacao(i, tm)
        cont += 1

    return pop_filhos

#funções para calcular a função objetivo
#transforma binarios para inteiros
def binToInt(bin): 
  dec = 0
  tam = len(bin)

  for x in range(tam):
    dec += (pow(2, x) * bin[(tam - 1) - x])

  return dec

#discretiza os valores
def discre(dec, bits):
  min = -2
  max = 2

  return min + ((max - min) / (pow(2, bits) - 1)) * dec

#função objetivo
def funcao_objetivo(ind):
    binario1 = ind[0:6]
    binario2 = ind[6:12]
    binario3 = ind[12:18]

    x1 = discre(binToInt(binario1), 6)
    x2 = discre(binToInt(binario2), 6)
    x3 = discre(binToInt(binario3), 6)

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

def main(n):
    resultados = []
    iteracao = []
    num_individuos = 100
    tam = 18
    tm = 10
    num_filhos = 100
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

        pop = torneio(pop, num_individuos)

        pop = nova_pop(pop, tam, tm, num_filhos, melhor)
        parada += 1 

    print(str(pop[indice]))
    print(str(funcao_objetivo(pop[indice])))
    print(parada)
    file1.write("\n------------------------------------------------------\n")

    file1.write(str(pop[indice]) + "\n")
    file1.write(str(funcao_objetivo(pop[indice])))
    file1.write("\n------------------------------------------------------\n")
    file1.write("O numero de geracoes foi: " + str(parada) + "\n")
    file1.close()

    plt.plot(iteracao, resultados)
    plt.show()


x = int(input("Digite o número de iterações: "))
main(x)