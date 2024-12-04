from colorama import Fore, Style, init
from typing import List, Set, Dict, Tuple, Optional, TextIO
import os

class WebSocketMazeVisualizer:
    """
    Creates a visual representation of the WebSocket maze.
    Supports both console output with colors and file output.
    """
    def __init__(self, vertices: Dict[int, Tuple[str, List[Tuple[int, float]]]], entrada: int):
        self.vertices = vertices
        self.entrada = entrada
        self.grid_size = self._calculate_grid_size()
        init(autoreset=True)

    def _calculate_grid_size(self) -> int:
        """Calculate grid size based on maximum vertex id"""
        max_vertex = max(self.vertices.keys())
        return int((max_vertex ** 0.5) + 1)

    def print_maze_connections(self, arquivo: Optional[TextIO] = None) -> None:
        """Print or write the maze connections in a list format"""
        lines = []
        for vertex_id in sorted(self.vertices.keys()):
            _, adjacents = self.vertices[vertex_id]
            connections = [f"({dest}, {int(weight)})" for dest, weight in sorted(adjacents)]
            line = f"Node {vertex_id} -> {', '.join(connections)}"
            if arquivo:
                arquivo.write(line + '\n')
            else:
                print(line)

    def exibir_labirinto(self,
                        caminho_percorrido: List[int] = None,
                        menor_caminho: List[int] = None,
                        arquivo: Optional[TextIO] = None) -> None:
        """
        Exibe o labirinto com a seguinte simbologia:
        - E: ponto de entrada
        - S: ponto de saída
        - █: caminho mínimo
        - Θ: caminho percorrido
        - n: peso da aresta (número inteiro)
        """
        if arquivo is None:
            init(autoreset=True)

        conjunto_caminho_percorrido = set(caminho_percorrido) if caminho_percorrido else set()
        conjunto_menor_caminho = set(menor_caminho) if menor_caminho else set()

        linhas_labirinto = []

        # Índices das colunas
        linha_indices = "  " + ''.join(f"{x:2}" for x in range(self.grid_size))
        linhas_labirinto.append(linha_indices)

        # Gera o labirinto
        for y in range(self.grid_size):
            linha = f"{y:2} "
            for x in range(self.grid_size):
                vertex_id = y * self.grid_size + x

                if vertex_id not in self.vertices:
                    linha += "  "
                    continue

                vertex_type, adjacents = self.vertices[vertex_id]

                # Determina o símbolo
                if vertex_id == self.entrada:
                    simbolo = 'E'
                    if arquivo is None:
                        simbolo = f"{Fore.RED}E{Style.RESET_ALL}"
                elif vertex_type == "2":  # Saída
                    simbolo = 'S'
                    if arquivo is None:
                        simbolo = f"{Fore.RED}S{Style.RESET_ALL}"
                elif vertex_id in conjunto_menor_caminho:
                    simbolo = '█'
                    if arquivo is None:
                        simbolo = f"{Fore.BLUE}█{Style.RESET_ALL}"
                elif vertex_id in conjunto_caminho_percorrido:
                    simbolo = 'Θ'
                    if arquivo is None:
                        simbolo = f"{Fore.BLUE}Θ{Style.RESET_ALL}"
                else:
                    # Get minimum weight for display
                    weights = [int(w) for _, w in adjacents]
                    min_weight = min(weights) if weights else 0
                    simbolo = str(min_weight)
                    if arquivo is None:
                        simbolo = f"{Fore.WHITE}{min_weight}{Style.RESET_ALL}"

                linha += f"{simbolo:2} "
            linhas_labirinto.append(linha)

        # Escreve as linhas
        if arquivo:
            for linha in linhas_labirinto:
                arquivo.write(linha + '\n')
        else:
            for linha in linhas_labirinto:
                print(linha)

    def generate_html(self, menor_caminho: List[int] = None) -> str:
        """Generates HTML content for graph visualization"""
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Maze Visualization</title>
            <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.js"></script>
            <link href="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.css" rel="stylesheet" type="text/css" />
            <style type="text/css">
                .graph {
                    width: 900px;
                    height: 600px;
                    border: 1px solid lightgray;
                    margin: 20px;
                }
                .container {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Complete Maze Graph</h2>
                <div id="complete-graph" class="graph"></div>
                <h2>Shortest Path</h2>
                <div id="path-graph" class="graph"></div>
            </div>

            <script type="text/javascript">
                // Network visualization options
                const options = {
                    nodes: {
                        shape: 'circle',
                        size: 30,
                        font: {
                            size: 14
                        }
                    },
                    edges: {
                        arrows: {
                            to: true
                        },
                        font: {
                            size: 14,
                            align: 'middle'
                        }
                    },
                    physics: {
                        enabled: true,
                        solver: 'forceAtlas2Based'
                    }
                };

                // Complete graph data
                const completeNodes = new vis.DataSet(NODES_DATA);
                const completeEdges = new vis.DataSet(EDGES_DATA);

                // Create complete network
                const completeContainer = document.getElementById('complete-graph');
                const completeData = {
                    nodes: completeNodes,
                    edges: completeEdges
                };
                const completeNetwork = new vis.Network(completeContainer, completeData, options);

                // Path graph data
                const pathNodes = new vis.DataSet(PATH_NODES_DATA);
                const pathEdges = new vis.DataSet(PATH_EDGES_DATA);

                // Create path network
                const pathContainer = document.getElementById('path-graph');
                const pathData = {
                    nodes: pathNodes,
                    edges: pathEdges
                };
                const pathNetwork = new vis.Network(pathContainer, pathData, options);
            </script>
        </body>
        </html>
        """

        # Prepare nodes data for both graphs
        nodes_data = []
        path_nodes_data = []
        seen_path_nodes = set()

        for vertex_id, (vertex_type, _) in self.vertices.items():
            color = '#97C2FC'  # default color
            if vertex_id == self.entrada:
                label = f'{vertex_id} (E)'
                color = '#FF8080'  # entry color
            elif vertex_type == "2":
                label = f'{vertex_id} (S)'
                color = '#80FF80'  # exit color
            else:
                label = str(vertex_id)

            # Add to complete graph
            nodes_data.append(f"{{id: {vertex_id}, label: '{label}', color: '{color}'}}")

            # Add to path graph if it's in the shortest path
            if menor_caminho and vertex_id in menor_caminho:
                if vertex_id not in seen_path_nodes:
                    path_nodes_data.append(f"{{id: {vertex_id}, label: '{label}', color: '{color}'}}")
                    seen_path_nodes.add(vertex_id)

        # Prepare edges data for complete graph
        edges_data = []
        edge_id = 0
        for vertex_id, (_, adjacents) in self.vertices.items():
            for dest, weight in adjacents:
                edges_data.append(
                    f"{{id: {edge_id}, from: {vertex_id}, to: {dest}, label: '{int(weight)}', arrows: 'to'}}"
                )
                edge_id += 1

        # Prepare edges data for path graph
        path_edges_data = []
        if menor_caminho:
            edge_id = 0
            for i in range(len(menor_caminho) - 1):
                current = menor_caminho[i]
                next_vertex = menor_caminho[i + 1]
                # Find weight for this edge
                _, adjacents = self.vertices[current]
                for dest, weight in adjacents:
                    if dest == next_vertex:
                        path_edges_data.append(
                            f"{{id: {edge_id}, from: {current}, to: {next_vertex}, " +
                            f"label: '{int(weight)}', arrows: 'to', color: '#FF0000'}}"
                        )
                        edge_id += 1
                        break

        # Replace placeholders in template
        html_content = html_template.replace('NODES_DATA', f"[{', '.join(nodes_data)}]")
        html_content = html_content.replace('EDGES_DATA', f"[{', '.join(edges_data)}]")
        html_content = html_content.replace('PATH_NODES_DATA', f"[{', '.join(path_nodes_data)}]")
        html_content = html_content.replace('PATH_EDGES_DATA', f"[{', '.join(path_edges_data)}]")

        return html_content

def create_visualizer(visited_states: Dict[int, Tuple[str, List[Tuple[int, float]]]],
                     entrada: int) -> WebSocketMazeVisualizer:
    """Creates a new WebSocketMazeVisualizer instance"""
    return WebSocketMazeVisualizer(visited_states, entrada)

def print_full_maze_analysis(visualizer: WebSocketMazeVisualizer,
                           caminho_percorrido: List[int],
                           menor_caminho: List[int],
                           maze_id: str,
                           arquivo: Optional[TextIO] = None) -> None:
    """
    Prints complete maze analysis and generates HTML visualization
    Creates files in ./results/maze_{maze_id}/
    """
    # Create results directory structure
    base_dir = os.path.join(".", "results")
    maze_dir = os.path.join(base_dir, f"maze_{maze_id}")

    # Create directories if they don't exist
    os.makedirs(maze_dir, exist_ok=True)

    # File paths
    txt_path = os.path.join(maze_dir, "saida_labirinto.txt")
    html_path = os.path.join(maze_dir, "maze_visualization.html")

    # Save text output
    with open(txt_path, 'w', encoding='utf-8') as arquivo:
        print("\nMaze Connections:", file=arquivo)
        visualizer.print_maze_connections(arquivo)

        print("\nBasic Maze Structure:", file=arquivo)
        visualizer.exibir_labirinto(arquivo=arquivo)

        print("\nComplete Exploration Path:", file=arquivo)
        visualizer.exibir_labirinto(caminho_percorrido=caminho_percorrido, arquivo=arquivo)
        print(' -> '.join(map(str, caminho_percorrido)))
        print(f'Steps Taken {len(caminho_percorrido)}')

        print("\nMinimum Path Found:", file=arquivo)
        visualizer.exibir_labirinto(menor_caminho=menor_caminho, arquivo=arquivo)
        print(' -> '.join(map(str, menor_caminho)))
        print(f'Steps Taken {len(menor_caminho)}')

    # Generate and save HTML visualization
    html_content = visualizer.generate_html(menor_caminho)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    # Print to console
    print("\nMaze Connections:")
    visualizer.print_maze_connections()

    print("\nBasic Maze Structure:")
    visualizer.exibir_labirinto()

    print("\nComplete Exploration Path:")
    visualizer.exibir_labirinto(caminho_percorrido=caminho_percorrido)
    print(' -> '.join(map(str, caminho_percorrido)))
    print(f'Steps Taken {len(caminho_percorrido)}')

    print("\nMinimum Path Found:")
    print(' -> '.join(map(str, menor_caminho)))
    print(f'Steps Taken {len(menor_caminho)}')

    print(f"\nResults saved in: {maze_dir}")
    print(f"- Text output: {txt_path}")
    print(f"- HTML visualization: {html_path}")
