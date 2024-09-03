import numpy as np
from random import randint
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import imageio.v2 as imageio

class Particula:
    def __init__(self, Xmin, Xmax, Vmin, Vmax, c1, c2, n, w):

        self.Xmin = Xmin
        self.Xmax = Xmax
        self.Vmin = Vmin
        self.Vmax = Vmax
        self.c1 = c1
        self.c2 = c2
        self.n = n
        self.w = w

        self.X = np.random.uniform(self.Xmin, self.Xmax, n)
        self.V = np.random.uniform(self.Vmin, self.Vmax, n)
        self.Pbest = self.X
        self.f = self.funcao_objetivo()

    def funcao_objetivo(self):
        t1 = -20 * np.exp(-0.2 * np.sqrt(np.sum(self.X**2) / self.n))
        t2 = -np.exp(np.sum(np.cos(2 * np.pi * self.X)) / self.n)
        return t1 + t2 + 20 + np.e
    
    def atualiza_velocidade(self, gbest):
        r1, r2 = np.random.rand(), np.random.rand()
        aux = (self.w * self.V + 
                  self.c1 * r1 * (self.Pbest - self.X) +
                  self.c2 * r2 * (gbest - self.X))
        self.V = np.clip(aux, self.Vmin, self.Vmax)

    def atualiza_posicao(self, gbest, gbestf):
        aux = self.X + self.V
        self.X = np.clip(aux, self.Xmin, self.Xmax)

        f = self.funcao_objetivo()
        if f < self.f:
            self.Pbest = self.X
            self.f = f
            if f < gbestf:
                gbest = self.X
                gbestf = f

class Enxame:
    def __init__(self, Xmin, Xmax, Vmin, Vmax, c1, c2, k, m, n, w):
        
        self.Xmin = Xmin
        self.Xmax = Xmax
        self.Vmin = Vmin
        self.Vmax = Vmax
        self.c1 = c1
        self.c2 = c2
        self.k = k
        self.m = m
        self.n = n
        self.w = w

        self.particulas = []
        self.history = []
        
        self.gbest = None
        self.gbestf = None

    def inicializar(self):
        for i in range(self.m):
            p = Particula(self.Xmin, self.Xmax, self.Vmin, self.Vmax, self.c1, self.c2, self.n, self.w)
            self.particulas.append(p)
        self.gbest = self.particulas[0].X
        self.gbestf = self.particulas[0].funcao_objetivo()
        
    def PSO(self):
        self.inicializar()

        for i in range(self.k):
            current_positions = np.array([p.X for p in self.particulas])
            self.history.append(current_positions)
            
            for p in self.particulas:
                p.atualiza_velocidade(self.gbest)
                p.atualiza_posicao(self.gbest, self.gbestf)
        return self.gbest, self.gbestf
    
    def save_gif(self, filename='pso_evolution.gif'):
        if self.n > 3:
            print(f"impossível plotar gráfico para dimensões superiores a 3.")
            return
            
        elif self.n == 3:
            with imageio.get_writer(filename, mode='I', duration=0.5) as writer:
                cont = 0
                for positions in self.history:
                    print(cont)
                    cont += 1
                    fig = plt.figure(figsize=(8, 6))
                    ax = fig.add_subplot(111, projection='3d')
                    ax.scatter(positions[:, 0], positions[:, 1], positions[:, 2])
                    ax.set_xlim(self.Xmin, self.Xmax)
                    ax.set_ylim(self.Xmin, self.Xmax)
                    ax.set_zlim(self.Xmin, self.Xmax)
                    ax.set_title(f'Iteração: {cont}')
                    ax.set_xlabel('Dimensão 1')
                    ax.set_ylabel('Dimensão 2')
                    ax.set_zlabel('Dimensão 3')
                    plt.grid(True)
                    
                    plt.savefig('temp.png')
                    plt.close()

                    image = imageio.imread('temp.png')
                    writer.append_data(image)
                    
        elif self.n == 2:
            with imageio.get_writer(filename, mode='I', duration=0.5) as writer:
                cont = 0
                for positions in self.history:
                    print(cont)
                    cont += 1
                    plt.figure(figsize=(6, 6))
                    plt.scatter(positions[:, 0], positions[:, 1])
                    plt.xlim(self.Xmin, self.Xmax)
                    plt.ylim(self.Xmin, self.Xmax)
                    plt.title(f'Iteração: {cont}')
                    plt.xlabel('Dimensão 1')
                    plt.ylabel('Dimensão 2')
                    plt.grid(True)
                    
                    plt.savefig('temp.png')
                    plt.close()
                    
                    image = imageio.imread('temp.png')
                    writer.append_data(image)
                    
E = Enxame(-2.0, 2.0, -1.0, 1.0, 1.5, 2.0, 200, 100, 3, 0.7)
gbest, gbestf = E.PSO()
E.save_gif()
print(gbest, gbestf)