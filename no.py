# no.py

class No:
    """
    Classe auxiliar para o algoritmo A*, representando um nó no grafo.
    """

    def __init__(self, posicao, g, h):
        self.posicao = posicao
        self.g = g  # Custo do caminho desde o início até este nó
        self.h = h  # Heurística (estimativa) até o objetivo
        self.f = g + h  # Função de avaliação
        self.pai = None  # Nó predecessor

    def __lt__(self, outro):
        return self.f < outro.f
