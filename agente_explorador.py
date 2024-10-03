# agente_explorador.py

import heapq
from no import No

class AgenteExplorador:
    """
    Classe que representa o agente que explora o labirinto.
    """

    def __init__(self, labirinto):
        self.labirinto = labirinto
        self.posicao_atual = (1, 1)  # Posição inicial
        self.objetivo = (labirinto.largura - 2, labirinto.altura - 2)  # Posição de saída
        self.vertices_explorados = set()
        self.caminho_percorrido = []
        self.grafo_explorado = {}
        self.movimentos = 0

    def heuristica(self, posicao):
        """
        Calcula a heurística (distância de Manhattan) até o objetivo.
        """
        x1, y1 = posicao
        x2, y2 = self.objetivo
        return abs(x1 - x2) + abs(y1 - y2)

    def explorar(self):
        """
        Explora o labirinto utilizando o algoritmo A*.
        """
        fila_prioridade = []
        no_inicial = No(self.posicao_atual, g=0, h=self.heuristica(self.posicao_atual))
        heapq.heappush(fila_prioridade, no_inicial)
        self.grafo_explorado[self.posicao_atual] = no_inicial

        while fila_prioridade:
            no_atual = heapq.heappop(fila_prioridade)
            self.posicao_atual = no_atual.posicao
            self.movimentos += 1

            if self.posicao_atual == self.objetivo:
                print("Saída encontrada!")
                caminho = self.construir_caminho(no_atual)
                print("Menor caminho:", caminho)
                print("Movimentos necessários:", len(caminho) - 1)
                return

            self.vertices_explorados.add(self.posicao_atual)
            vizinhos = self.labirinto.obter_vizinhos(*self.posicao_atual)
            for vizinho_pos in vizinhos:
                if vizinho_pos in self.vertices_explorados:
                    continue
                g = no_atual.g + 1  # Custo do movimento
                h = self.heuristica(vizinho_pos)
                no_vizinho = No(vizinho_pos, g, h)
                no_vizinho.pai = no_atual

                if vizinho_pos not in self.grafo_explorado or g < self.grafo_explorado[vizinho_pos].g:
                    heapq.heappush(fila_prioridade, no_vizinho)
                    self.grafo_explorado[vizinho_pos] = no_vizinho

    def construir_caminho(self, no):
        """
        Reconstrói o caminho desde o início até o nó dado.
        """
        caminho = []
        while no is not None:
            caminho.append(no.posicao)
            no = no.pai
        return caminho[::-1]
