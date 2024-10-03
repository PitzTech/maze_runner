# main.py

from labirinto import Labirinto
from agente_explorador import AgenteExplorador

def main():
    largura = 21  # Deve ser um número ímpar
    altura = 21   # Deve ser um número ímpar

    labirinto = Labirinto(largura, altura)
    # labirinto.exibir_labirinto()  # Descomente para visualizar o labirinto

    agente = AgenteExplorador(labirinto)
    agente.explorar()

if __name__ == "__main__":
    main()
