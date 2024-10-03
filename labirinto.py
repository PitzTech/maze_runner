# labirinto.py

import random

class Labirinto:
    """
    Classe que representa o labirinto como uma grade bidimensional.
    """

    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura
        self.matriz = [[1 for _ in range(largura)] for _ in range(altura)]
        self.gerar_labirinto()

    def gerar_labirinto(self):
        """
        Gera um labirinto aleatório utilizando o algoritmo de recursão com backtracking.
        """
        def dentro_do_labirinto(x, y):
            return 0 <= x < self.largura and 0 <= y < self.altura

        def carve_passages(x, y):
            direcoes = [(0, -1), (1, 0), (0, 1), (-1, 0)]
            random.shuffle(direcoes)
            for dx, dy in direcoes:
                nx, ny = x + dx * 2, y + dy * 2
                if dentro_do_labirinto(nx, ny) and self.matriz[ny][nx] == 1:
                    self.matriz[ny - dy][nx - dx] = 0
                    self.matriz[ny][nx] = 0
                    carve_passages(nx, ny)

        # Inicia no canto superior esquerdo
        self.matriz[1][1] = 0
        carve_passages(1, 1)

    def obter_vizinhos(self, x, y):
        """
        Retorna uma lista de vizinhos acessíveis a partir da posição (x, y).
        """
        vizinhos = []
        direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in direcoes:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.largura and 0 <= ny < self.altura:
                if self.matriz[ny][nx] == 0:
                    vizinhos.append((nx, ny))
        return vizinhos

    def exibir_labirinto(self):
        """
        Exibe o labirinto no console.
        """
        for linha in self.matriz:
            print(''.join(['█' if celula == 1 else ' ' for celula in linha]))
