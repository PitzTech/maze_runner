# Solucionador de Labirintos

Este projeto implementa um solucionador de labirintos em Python utilizando o algoritmo A* para encontrar o menor caminho entre a entrada e a saída.

## Estrutura do Projeto

- **`labirinto.py`**: Classe `Labirinto` para gerar e representar o labirinto.
- **`agente_explorador.py`**: Classe `AgenteExplorador` que implementa o algoritmo de exploração.
- **`main.py`**: Ponto de entrada do programa.
- **`.gitignore`**: Arquivo para especificar quais arquivos ou pastas o Git deve ignorar.
- **`README.md`**: Documentação do projeto.

## Requisitos

- Python 3.x

## Como Executar

1. Clone o repositório ou baixe os arquivos.
2. Navegue até o diretório do projeto.
3. Execute os seguintes comandos:

  ```bash
  python3 -m venv venv
  source venv/bin/activate  # No Windows, use venv\Scripts\activate
  pip install --upgrade pip
  pip install -r requirements.txt
  ```

   ```bash
   python main.py
   ```

## Personalização

1. Tamanho do Labirinto: Você pode alterar o tamanho do labirinto modificando as variáveis largura e altura no arquivo main.py. Certifique-se de que sejam números ímpares.

2. Visualização: Para visualizar o labirinto gerado no console, descomente a linha labirinto.exibir_labirinto() no arquivo main.py.
