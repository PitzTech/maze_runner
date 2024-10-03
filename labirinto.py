import random
from colorama import Fore, Back, Style, init

class Labirinto:
    """
    Classe que representa o labirinto como uma grade bidimensional.
    """

    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura
        self.matriz = [[1 for _ in range(largura)] for _ in range(altura)]
        self.gerar_labirinto()
        self.entrada = self.definir_entrada()
        self.saida = self.definir_saida()

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

        # Inicia em uma posição aleatória
        start_x = random.randrange(1, self.largura, 2)
        start_y = random.randrange(1, self.altura, 2)
        self.matriz[start_y][start_x] = 0
        carve_passages(start_x, start_y)

    def definir_entrada(self):
        """
        Define uma posição aleatória como entrada (em uma célula vazia).
        """
        while True:
            x = random.randrange(1, self.largura, 2)
            y = random.randrange(1, self.altura, 2)
            if self.matriz[y][x] == 0:
                return (x, y)

    def definir_saida(self):
        """
        Define uma posição aleatória como saída (em uma célula vazia diferente da entrada).
        """
        while True:
            x = random.randrange(1, self.largura, 2)
            y = random.randrange(1, self.altura, 2)
            if self.matriz[y][x] == 0 and (x, y) != self.entrada:
                return (x, y)

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

    def exibir_labirinto(self, caminho_percorrido=None, menor_caminho=None):
        """
        Exibe o labirinto no console, incluindo referências numéricas para as posições
        e destacando a entrada e a saída em vermelho. Destaca o caminho percorrido em verde
        e o menor caminho em azul, se fornecidos.
        """
        init(autoreset=True)  # Inicializa o colorama

        entrada = self.entrada
        saida = self.saida

        # Converte as listas de caminhos em conjuntos para melhorar a eficiência de busca
        conjunto_caminho_percorrido = set(caminho_percorrido) if caminho_percorrido else set()
        conjunto_menor_caminho = set(menor_caminho) if menor_caminho else set()

        # Imprime os índices das colunas
        print("   ", end='')
        for x in range(self.largura):
            print(f"{x % 10}", end='')
        print()

        for y in range(self.altura):
            # Imprime o índice da linha
            print(f"{y % 10:2} ", end='')
            for x in range(self.largura):
                celula = self.matriz[y][x]
                posicao_atual = (x, y)
                if posicao_atual == entrada:
                    # Destaca a entrada em vermelho com 'E'
                    print(f"{Fore.RED}E{Style.RESET_ALL}", end='')
                elif posicao_atual == saida:
                    # Destaca a saída em vermelho com 'S'
                    print(f"{Fore.RED}S{Style.RESET_ALL}", end='')
                elif posicao_atual in conjunto_menor_caminho:
                    # Destaca o menor caminho em azul
                    print(f"{Fore.BLUE}·{Style.RESET_ALL}", end='')
                elif posicao_atual in conjunto_caminho_percorrido:
                    # Destaca o caminho percorrido em verde
                    print(f"{Fore.GREEN}·{Style.RESET_ALL}", end='')
                elif celula == 1:
                    print('█', end='')
                else:
                    print(' ', end='')
            print()

    def eh_saida(self, posicao):
        """
        Verifica se a posição dada é a saída.
        """
        return posicao == self.saida
