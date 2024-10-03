import random

class AgenteExplorador:
    """
    Classe que representa o agente que explora o labirinto.
    O agente move-se passo a passo, descobrindo novos vértices apenas ao visitá-los.
    Ele não conhece a posição da saída até alcançá-la.
    """

    def __init__(self, labirinto):
        self.labirinto = labirinto
        self.posicao_atual = labirinto.entrada  # Posição inicial
        self.vertices_visitados = set()
        self.movimentos = 0
        self.caminho_percorrido = []  # Todas as posições que o agente passou
        self.pilha_caminho = []  # Pilha para simular a movimentação e backtracking
        self.saida_encontrada = False
        self.saida = None  # Será definida quando a saída for encontrada

    def explorar(self):
        """
        Explora o labirinto utilizando uma abordagem de DFS iterativa,
        simulando a movimentação passo a passo do agente, incluindo backtracking.
        """
        self.pilha_caminho.append(self.posicao_atual)
        self.vertices_visitados.add(self.posicao_atual)
        self.caminho_percorrido.append(self.posicao_atual)
        self.movimentos += 1

        while self.pilha_caminho:
            posicao_atual = self.pilha_caminho[-1]
            # Verifica se a posição atual é a saída
            if self.labirinto.eh_saida(posicao_atual):
                self.saida_encontrada = True
                self.saida = posicao_atual
                print("Saída encontrada!")
                menor_caminho = self.pilha_caminho.copy()
                print("Menor caminho:", menor_caminho)
                print("Movimentos necessários:", self.movimentos)
                break

            # Obtém os vizinhos não visitados da posição atual
            vizinhos = self.labirinto.obter_vizinhos(posicao_atual[0], posicao_atual[1])
            vizinhos_nao_visitados = [v for v in vizinhos if v not in self.vertices_visitados]

            if vizinhos_nao_visitados:
                # Escolhe um vizinho não visitado para mover
                proximo_passo = random.choice(vizinhos_nao_visitados)
                # Move para o próximo passo
                self.pilha_caminho.append(proximo_passo)
                self.vertices_visitados.add(proximo_passo)
                self.caminho_percorrido.append(proximo_passo)
                self.movimentos += 1
            else:
                # Não há vizinhos não visitados, precisa voltar (backtracking)
                self.pilha_caminho.pop()
                if self.pilha_caminho:
                    # Move de volta para a posição anterior
                    self.caminho_percorrido.append(self.pilha_caminho[-1])
                    self.movimentos += 1
        else:
            print("Não foi possível encontrar a saída.")

    def get_caminho_percorrido(self):
        """
        Retorna o caminho percorrido pelo agente, incluindo backtracking.
        """
        return self.caminho_percorrido

    def get_menor_caminho(self):
        """
        Retorna o menor caminho encontrado até a saída.
        """
        if self.saida_encontrada:
            return self.pilha_caminho.copy()
        else:
            return []
