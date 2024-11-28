import random
import asyncio
from typing import List, Tuple, Set, Optional, Dict
from collections import defaultdict

class AgenteExplorador:
    """
    Class that represents the agent that explores the maze.
    The agent moves step by step, discovering new vertices only when visiting them.
    It doesn't know the exit position until reaching it.
    This version supports:
    - Local and websocket mazes
    - Weighted edges
    - Directional graphs
    """

    def __init__(self, labirinto, imprimir_passos_no_arquivo=False, nome_arquivo='saida_labirinto.txt'):
        self.labirinto = labirinto
        self.posicao_atual = labirinto.entrada  # Initial position
        self.vertices_visitados: Set = set()
        self.movimentos = 0
        self.peso_total = 0  # Total weight of the path
        self.caminho_percorrido: List[Tuple[int, int, float]] = []  # Now stores (from_vertex, to_vertex, weight)
        self.pilha_caminho: List[int] = []  # Stack to simulate movement and backtracking
        self.pesos_caminhos: Dict[Tuple[int, int], float] = {}  # Stores weights between vertices
        self.saida_encontrada = False
        self.saida = None  # Will be defined when exit is found
        self.passo = 0  # Step counter for display
        self.imprimir_passos_no_arquivo = imprimir_passos_no_arquivo
        self.nome_arquivo = nome_arquivo

        if self.imprimir_passos_no_arquivo:
            self.arquivo = open(self.nome_arquivo, 'w', encoding='utf-8')
        else:
            self.arquivo = None

    async def explorar(self):
        """
        Explores the maze using an iterative DFS approach with weighted paths.
        Supports directional movement and weighted edges.
        """
        self.pilha_caminho.append(self.posicao_atual)
        self.vertices_visitados.add(self.posicao_atual)
        self.movimentos += 1
        self.passo += 1

        if self.imprimir_passos_no_arquivo:
            self._write_step_to_file()

        while self.pilha_caminho:
            posicao_atual = self.pilha_caminho[-1]

            # Check if current position is exit
            if self.labirinto.eh_saida(posicao_atual):
                self._handle_exit_found()
                break

            # Get available neighbors with weights
            vizinhos = await self._get_vizinhos_com_peso(posicao_atual)
            vizinhos_nao_visitados = [(v, w) for v, w in vizinhos if v not in self.vertices_visitados]

            if vizinhos_nao_visitados:
                # Choose next step (can implement different strategies here)
                proximo_vertice, peso = self._escolher_proximo_passo(vizinhos_nao_visitados)

                # Move to next vertex
                await self._mover_para(proximo_vertice)

                # Update path information
                self.pilha_caminho.append(proximo_vertice)
                self.vertices_visitados.add(proximo_vertice)
                self.caminho_percorrido.append((posicao_atual, proximo_vertice, peso))
                self.pesos_caminhos[(posicao_atual, proximo_vertice)] = peso
                self.peso_total += peso
                self.movimentos += 1
                self.passo += 1

                if self.imprimir_passos_no_arquivo:
                    self._write_step_to_file()
            else:
                # Backtrack
                vertice_atual = self.pilha_caminho.pop()
                if self.pilha_caminho:
                    vertice_anterior = self.pilha_caminho[-1]
                    await self._mover_para(vertice_anterior)

                    # Update path for backtracking
                    peso_volta = self.pesos_caminhos.get((vertice_atual, vertice_anterior),
                                                       self.pesos_caminhos.get((vertice_anterior, vertice_atual), 1))
                    self.caminho_percorrido.append((vertice_atual, vertice_anterior, peso_volta))
                    self.peso_total += peso_volta
                    self.movimentos += 1
                    self.passo += 1

                    if self.imprimir_passos_no_arquivo:
                        self._write_step_to_file()
        else:
            self._handle_no_exit_found()

        if self.imprimir_passos_no_arquivo and self.arquivo:
            self.arquivo.close()

    async def _get_vizinhos_com_peso(self, vertice: int) -> List[Tuple[int, float]]:
        """
        Gets neighbors with their weights. Handles both local and websocket mazes.
        """
        if hasattr(self.labirinto, 'obter_vizinhos_com_peso'):
            return self.labirinto.obter_vizinhos_com_peso(vertice)
        else:
            # For backward compatibility with unweighted mazes
            vizinhos = self.labirinto.obter_vizinhos(vertice, 0)  # Changed signature to support vertices directly
            return [(v, 1.0) for v in vizinhos]  # Default weight of 1

    async def _mover_para(self, vertice: int):
        """
        Handles movement in both local and websocket mazes
        """
        if hasattr(self.labirinto, 'move_to'):
            current, vertex_type, adjacents = await self.labirinto.move_to(vertice)
            self.labirinto.current_vertex = current
            self.labirinto.vertex_type = vertex_type
            self.labirinto.adjacents = adjacents

    def _escolher_proximo_passo(self, vizinhos: List[Tuple[int, float]]) -> Tuple[int, float]:
        """
        Strategy for choosing next step. Can be modified to implement different strategies.
        Currently implements random choice but considers weights.
        """
        return random.choice(vizinhos)

    def _write_step_to_file(self):
        """
        Writes the current step information to file
        """
        self.arquivo.write(f"\nPasso {self.passo}:\n")
        self.arquivo.write(f"Posição atual: {self.pilha_caminho[-1]}\n")
        self.arquivo.write(f"Peso total do caminho: {self.peso_total}\n")
        if hasattr(self.labirinto, 'exibir_labirinto'):
            self.labirinto.exibir_labirinto(
                agente_posicao=self.pilha_caminho[-1],
                caminho_percorrido=[x[0] for x in self.caminho_percorrido],
                arquivo=self.arquivo
            )

    def _handle_exit_found(self):
        """
        Handles the case when exit is found
        """
        self.saida_encontrada = True
        self.saida = self.pilha_caminho[-1]
        message = (
            f"Exit found!\n"
            f"Shortest path: {self.pilha_caminho}\n"
            f"Total weight: {self.peso_total}\n"
            f"Moves needed: {self.movimentos}"
        )
        if self.imprimir_passos_no_arquivo:
            self.arquivo.write(message)
        print(message)

    def _handle_no_exit_found(self):
        """
        Handles the case when no exit is found
        """
        message = "Could not find exit."
        if self.imprimir_passos_no_arquivo:
            self.arquivo.write(message)
        print(message)

    def get_caminho_percorrido(self) -> List[Tuple[int, int, float]]:
        """
        Returns the path traveled by the agent, including backtracking.
        Now includes weights in the path information.
        """
        return self.caminho_percorrido

    def get_menor_caminho(self) -> Tuple[List[int], float]:
        """
        Returns the shortest path found to the exit and its total weight.
        """
        if self.saida_encontrada:
            return self.pilha_caminho.copy(), self.peso_total
        return [], 0.0
