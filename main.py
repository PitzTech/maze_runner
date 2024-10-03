from labirinto import Labirinto
from agente_explorador import AgenteExplorador
import random

def main():
    # Gera dimensões aleatórias ímpares entre 11 e 31
    largura = random.randrange(11, 32, 2)
    altura = random.randrange(11, 32, 2)

    print(f"Labirinto de tamanho {largura}x{altura}")

    print("Labirinto inicial:")
    labirinto = Labirinto(largura, altura)
    labirinto.exibir_labirinto()

    # Cria o agente, com a flag para imprimir ou não os passos no arquivo
    agente = AgenteExplorador(labirinto, imprimir_passos_no_arquivo=True)  # Ajuste aqui a flag
    agente.explorar()

      # Após a exploração, imprime o labirinto final no console com cores
    print("\nLabirinto com o caminho percorrido em azul e o menor caminho em vermelho:")
    labirinto.exibir_labirinto(
        caminho_percorrido=agente.get_caminho_percorrido(),
        menor_caminho=agente.get_menor_caminho()
    )

    print(f"\nTotal de movimentos realizados: {agente.movimentos}")

    if agente.imprimir_passos_no_arquivo:
        print("Exploração detalhada foi escrita no arquivo 'saida_labirinto.txt'.")

if __name__ == "__main__":
    main()
