import random

class AgenteExplorador:
    """
    Classe que representa o agente que explora o labirinto.
    O agente move-se passo a passo, descobrindo novos vértices apenas ao visitá-los.
    Ele não conhece a posição da saída até alcançá-la.
    """

    def __init__(self, labirinto, imprimir_passos_no_arquivo=False, nome_arquivo='saida_labirinto.txt'):
        self.labirinto = labirinto
        self.posicao_atual = labirinto.entrada  # Posição inicial
        self.vertices_visitados = set()
        self.movimentos = 0
        self.caminho_percorrido = []  # Todas as posições que o agente passou
        self.pilha_caminho = []  # Pilha para simular a movimentação e backtracking
        self.saida_encontrada = False
        self.saida = None  # Será definida quando a saída for encontrada
        self.passo = 0  # Contador de passos para exibição
        self.imprimir_passos_no_arquivo = imprimir_passos_no_arquivo  # Flag para controlar a escrita no arquivo
        self.nome_arquivo = nome_arquivo  # Nome do arquivo para escrever as saídas

        if self.imprimir_passos_no_arquivo:
            # Abre o arquivo em modo de escrita
            self.arquivo = open(self.nome_arquivo, 'w', encoding='utf-8')
        else:
            self.arquivo = None

    def explorar(self):
        """
        Explora o labirinto utilizando uma abordagem de DFS iterativa,
        simulando a movimentação passo a passo do agente, incluindo backtracking.
        As saídas são escritas em um arquivo se a flag estiver ativada.
        """
        self.pilha_caminho.append(self.posicao_atual)
        self.vertices_visitados.add(self.posicao_atual)
        self.caminho_percorrido.append(self.posicao_atual)
        self.movimentos += 1
        self.passo += 1

        # Escreve o labirinto após o primeiro passo se a flag estiver ativada
        if self.imprimir_passos_no_arquivo:
            self.arquivo.write(f"\nPasso {self.passo}:\n")
            self.labirinto.exibir_labirinto(agente_posicao=self.posicao_atual,
                                            caminho_percorrido=self.caminho_percorrido,
                                            arquivo=self.arquivo)

        while self.pilha_caminho:
            posicao_atual = self.pilha_caminho[-1]
            # Verifica se a posição atual é a saída
            if self.labirinto.eh_saida(posicao_atual):
                self.saida_encontrada = True
                self.saida = posicao_atual
                if self.imprimir_passos_no_arquivo:
                    self.arquivo.write("Saída encontrada!\n")
                    menor_caminho = self.pilha_caminho.copy()
                    self.arquivo.write(f"Menor caminho: {menor_caminho}\n")
                    self.arquivo.write(f"Movimentos necessários: {self.movimentos}\n")
                else:
                    menor_caminho = self.pilha_caminho.copy()
                print("Saída encontrada!")
                print(f"Menor caminho: {menor_caminho}")
                print(f"Movimentos necessários: {self.movimentos}")
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
                self.passo += 1
                # Escreve o labirinto após o movimento se a flag estiver ativada
                if self.imprimir_passos_no_arquivo:
                    self.arquivo.write(f"\nPasso {self.passo}:\n")
                    self.labirinto.exibir_labirinto(agente_posicao=proximo_passo,
                                                    caminho_percorrido=self.caminho_percorrido,
                                                    arquivo=self.arquivo)
            else:
                # Não há vizinhos não visitados, precisa voltar (backtracking)
                self.pilha_caminho.pop()
                if self.pilha_caminho:
                    # Move de volta para a posição anterior
                    self.caminho_percorrido.append(self.pilha_caminho[-1])
                    self.movimentos += 1
                    self.passo += 1
                    # Escreve o labirinto após o movimento de backtracking se a flag estiver ativada
                    if self.imprimir_passos_no_arquivo:
                        self.arquivo.write(f"\nPasso {self.passo}:\n")
                        self.labirinto.exibir_labirinto(agente_posicao=self.pilha_caminho[-1],
                                                        caminho_percorrido=self.caminho_percorrido,
                                                        arquivo=self.arquivo)
        else:
            if self.imprimir_passos_no_arquivo:
                self.arquivo.write("Não foi possível encontrar a saída.\n")
            print("Não foi possível encontrar a saída.")

        # Fecha o arquivo após a exploração
        if self.imprimir_passos_no_arquivo and self.arquivo:
            self.arquivo.close()

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
