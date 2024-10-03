from labirinto import Labirinto
from agente_explorador import AgenteExplorador
import random

def main():
    # Gera dimensões aleatórias ímpares entre 11 e 31
    largura = random.randrange(11, 32, 2)
    altura = random.randrange(11, 32, 2)

    print(f"Labirinto de tamanho {largura}x{altura}")

    labirinto = Labirinto(largura, altura)
    labirinto.exibir_labirinto()

    agente = AgenteExplorador(labirinto)
    agente.explorar()

    # Exibe o labirinto novamente com os caminhos destacados
    print("\nLabirinto com o caminho percorrido em verde e o menor caminho em azul:")
    labirinto.exibir_labirinto(
        caminho_percorrido=agente.get_caminho_percorrido(),
        menor_caminho=agente.get_menor_caminho()
    )

if __name__ == "__main__":
    main()
