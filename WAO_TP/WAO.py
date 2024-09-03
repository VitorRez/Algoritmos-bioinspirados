import numpy as np
import matplotlib.pyplot as plt
import imageio.v2 as imageio

class Baleia:
    def __init__(self, Xmin, Xmax, n):
        self.Xmin = Xmin
        self.Xmax = Xmax
        self.n = n

        self.X = np.random.uniform(self.Xmin, self.Xmax, n)
        self.fitness = self.funcao_objetivo()

    def funcao_objetivo(self):
        t1 = -20 * np.exp(-0.2 * np.sqrt(np.sum(self.X**2) / self.n))
        t2 = -np.exp(np.sum(np.cos(2 * np.pi * self.X)) / self.n)
        return t1 + t2 + 20 + np.e
    
    def cercamento(self, melhor_baleia, A, D):
        self.X = melhor_baleia - A * D

    def espiral_de_bolhas(self, melhor_baleia, D):
        l = np.random.uniform(-1, 1)
        self.X = D * np.exp(l) * np.cos(2 * np.pi * l) + melhor_baleia
    
    def buscar_novas_presas(self, Xrand, A, D):
        self.X = Xrand - A * D

    def atualizar_posicao(self, melhor_baleia, A, C, p, Xrand=None):
        D = np.abs(C * melhor_baleia - self.X)
        if p < 0.5:
            if np.all(np.abs(A) < 1):
                self.cercamento(melhor_baleia, A, D)
            else:
                if Xrand is not None:
                    self.buscar_novas_presas(Xrand, A, D)
        else:
            self.espiral_de_bolhas(melhor_baleia, D)

        self.X = np.clip(self.X, self.Xmin, self.Xmax)
        self.f = self.funcao_objetivo()            

#baleal é o coletivo de baleias, num é chique?
class Baleal: 
    def __init__(self, Xmin, Xmax, num_iter, num_baleia, n):
        self.Xmin = Xmin
        self.Xmax = Xmax
        self.num_iter = num_iter
        self.num_baleia = num_baleia
        self.n = n

        self.baleias = []
        self.history = []
        self.melhor_baleia = None
        self.melhor_f = None

    def inicializar(self):
        for i in range(self.num_baleia):
            baleia = Baleia(self.Xmin, self.Xmax, self.n)
            self.baleias.append(baleia)
        self.melhor_baleia = self.baleias[0].X
        self.melhor_f = self.baleias[0].funcao_objetivo()

    def WOA(self):
        self.inicializar()
        #r = np.random.uniform(0, 1, self.n)

        for i in range(self.num_iter):
            a = 2 * (1 - np.log(i + 1) / np.log(self.num_iter + 1)) # Decaimento de a
            for baleia in self.baleias:
                r = np.random.uniform(0, 1, self.n)
                A = 2*a * r - a
                C = 2 * r
                p = np.random.rand()
                Xrand = self.baleias[np.random.randint(self.num_baleia)].X
                
                baleia.atualizar_posicao(self.melhor_baleia, A, C, p, Xrand)

            for baleia in self.baleias:
                if baleia.f < self.melhor_f:
                    self.melhor_baleia = baleia.X
                    self.melhor_f = baleia.f

            current_positions = np.array([baleia.X for baleia in self.baleias])
            self.history.append(current_positions)
        
        return self.melhor_baleia, self.melhor_f
    
    def save_gif(self, filename="woa_evolution.gif"):
        with imageio.get_writer(filename, mode='I', duration=1) as writer:
                cont = 0
                for positions in self.history:
                    print(cont)
                    cont += 1
                    plt.figure(figsize=(6, 6))
                    plt.scatter(positions[:, 0], positions[:, 1])
                    plt.xlim(-3, 3)
                    plt.ylim(-3, 3)
                    plt.title(f'Iteração: {cont}')
                    plt.xlabel('Dimensão 1')
                    plt.ylabel('Dimensão 2')
                    plt.grid(True)
                    
                    plt.savefig('temp.png')
                    plt.close()
                    
                    image = imageio.imread('temp.png')
                    writer.append_data(image)

B = Baleal(-2.0, 2.0, 25, 500, 2)
melhor_b, melhor_f = B.WOA()
print(melhor_b, melhor_f)
B.save_gif()