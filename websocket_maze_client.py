import asyncio
import websockets
import re
from typing import List, Tuple, Optional, Dict, Set
from config import MazeConfig
from vertex_type import VertexType
from collections import defaultdict
import heapq
from maze_visualizer import create_visualizer, print_full_maze_analysis

class WebSocketLabirinto:
    def __init__(self, websocket, current_vertex: int, vertex_type: str, adjacents: List[Tuple[int, float]]):
        self.websocket = websocket
        self.current_vertex = current_vertex
        self.vertex_type = VertexType.from_value(vertex_type)
        self.entrada = current_vertex if self.vertex_type == VertexType.ENTRADA else None
        self.adjacents = self._remove_duplicate_edges(adjacents)
        self.visited_states: Dict[int, Tuple[str, List[Tuple[int, float]]]] = {
            current_vertex: (vertex_type, self.adjacents)
        }
        self.exits: Set[int] = set()
        if self.vertex_type == VertexType.SAIDA:
            self.exits.add(current_vertex)

    def _remove_duplicate_edges(self, adjacents: List[Tuple[int, float]]) -> List[Tuple[int, float]]:
        """Remove duplicate edges keeping only one instance of each destination"""
        seen = {}
        for dest, weight in adjacents:
            if dest not in seen or weight < seen[dest]:
                seen[dest] = weight
        return [(dest, weight) for dest, weight in seen.items()]

    async def move_to(self, vertex_id: int) -> Tuple[int, str, List[Tuple[int, float]]]:
        if vertex_id is None:
            raise ValueError("Cannot move to None vertex")

        command = f"ir: {vertex_id}"

        print(f"\n📍 Current State:")
        print(f"Vértice atual: {self.current_vertex}, Tipo: {self.vertex_type}")
        print(f"Adjacentes: {self.adjacents}")
        print(f"🔄 Moving to vertex {vertex_id}")

        await self.websocket.send(command)
        response = await self.websocket.recv()
        print(f"📩 Server response: {response}")

        if "Comando inválido" in response or "Vértice inválido" in response:
            raise ValueError(f"Invalid movement: {response}")

        current, vertex_type, adjacents = await self.parse_server_message(response)
        self.current_vertex = current
        self.vertex_type = VertexType.from_value(vertex_type)
        self.adjacents = self._remove_duplicate_edges(adjacents)
        self.visited_states[current] = (vertex_type, self.adjacents)

        if self.vertex_type == VertexType.SAIDA:
            self.exits.add(current)

        return current, vertex_type, self.adjacents

    @staticmethod
    async def parse_server_message(message: str) -> Tuple[int, str, List[Tuple[int, float]]]:
        pattern = r"Vértice atual: (\d+), Tipo: (\d+|normal|saida|entrada), Adjacentes\(Vertice, Peso\): \[(.*?)\]"
        match = re.match(pattern, message)
        if not match:
            raise ValueError(f"Invalid message format: {message}")

        current_vertex = int(match.group(1))
        vertex_type = match.group(2)
        adjacents_str = match.group(3)

        adjacents = []
        if adjacents_str:
            adj_pattern = r"\((\d+),\s*(\d+(?:\.\d+)?)\)"
            adjacents = [(int(v), float(w)) for v, w in re.findall(adj_pattern, adjacents_str)]

        return current_vertex, vertex_type, adjacents

    def eh_saida(self, vertex_id: int) -> bool:
        if vertex_id in self.visited_states:
            vertex_type, _ = self.visited_states[vertex_id]
            return VertexType.from_value(vertex_type) == VertexType.SAIDA
        return False

class WebSocketMazeSolver:
    def __init__(self, config: MazeConfig):
        self.config = config
        self.labirinto = None

    async def explore_maze(self) -> None:
      """Explores the entire maze before finding shortest path"""
      queue = [self.labirinto.current_vertex]
      visited = {self.labirinto.current_vertex}

      while queue:
          current = queue.pop(0)

          # Get adjacents for current vertex
          _, adjacents = self.labirinto.visited_states[current]

          # Move to current vertex if we're not already there
          if current != self.labirinto.current_vertex:
              await self.labirinto.move_to(current)

          # Check all adjacent vertices
          for next_vertex, _ in adjacents:
              if next_vertex not in visited:
                  visited.add(next_vertex)
                  queue.append(next_vertex)
                  await self.labirinto.move_to(next_vertex)
                  # Move back to continue exploration from current vertex
                  await self.labirinto.move_to(current)

    async def find_shortest_path(self, start: int) -> Tuple[List[int], float]:
        distances = defaultdict(lambda: float('infinity'))
        distances[start] = 0
        previous = {}
        pq = [(0, start)]
        visited = set()
        best_exit = None
        min_exit_distance = float('infinity')

        while pq:
            current_distance, current_vertex = heapq.heappop(pq)

            if current_vertex in visited:
                continue

            visited.add(current_vertex)

            if self.labirinto.eh_saida(current_vertex):
                if current_distance < min_exit_distance:
                    min_exit_distance = current_distance
                    best_exit = current_vertex

            # Get current vertex's adjacents
            _, adjacents = self.labirinto.visited_states[current_vertex]

            # Explore each adjacent vertex
            for next_vertex, weight in adjacents:
                if next_vertex not in visited:
                    distance = current_distance + weight

                    if distance < distances[next_vertex]:
                        distances[next_vertex] = distance
                        previous[next_vertex] = current_vertex
                        heapq.heappush(pq, (distance, next_vertex))

                    # Only explore unvisited vertices that are in our adjacents list
                    if next_vertex not in self.labirinto.visited_states:
                        try:
                            await self.labirinto.move_to(next_vertex)
                        except ValueError as e:
                            print(f"⚠️ Warning: Skipping invalid move to {next_vertex}")
                            continue

        if best_exit is not None:
            path = []
            current = best_exit
            while current in previous:
                path.append(current)
                current = previous[current]
            path.append(start)
            return path[::-1], min_exit_distance

        return [], 0.0

    async def explore(self) -> Tuple[List[int], float]:
        url = f"{self.config.websocket_url}{self.config.grupo_id}/{self.config.labirinto_id}"

        print("\n🌐 Starting WebSocket Maze Solver")
        print(f"📍 Connecting to: {url}")

        try:
            async with websockets.connect(url) as websocket:
                initial_message = await websocket.recv()
                print(f"\n📩 Initial server message: {initial_message}")

                current, vertex_type, adjacents = await WebSocketLabirinto.parse_server_message(initial_message)
                self.labirinto = WebSocketLabirinto(websocket, current, vertex_type, adjacents)

                # First explore the entire maze
                print("\n🔍 Exploring entire maze...")
                await self.explore_maze()

                # Now find the shortest path using the complete maze information
                print("\n🔍 Finding shortest path...")
                path, weight = await self.find_shortest_path(current)

                if path:
                    print("\n✨ Path found!")
                    print(f"Path: {path}")
                    print(f"Total weight: {weight}")

                    visualizer = create_visualizer(self.labirinto.visited_states, self.labirinto.entrada)

                    # Show in console
                    print_full_maze_analysis(
                        visualizer,
                        caminho_percorrido=list(self.labirinto.visited_states.keys()),
                        menor_caminho=path,
                        maze_id=self.config.labirinto_id
                    )

                    return path, weight
                else:
                    print("\n❌ No path found")
                    return [], 0.0

        except websockets.exceptions.WebSocketException as e:
            print(f"❌ WebSocket error: {e}")
            return [], 0.0
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            raise

if __name__ == "__main__":
    async def main():
        try:
            from config import load_maze_config
            config = load_maze_config()

            solver = WebSocketMazeSolver(config)
            path, weight = await solver.explore()

            print("\n🏁 Final Results:")
            print(f"📍 Path: {path}")
            print(f"⚖️  Total weight: {weight}")

        except ValueError as e:
            print(f"❌ Configuration error: {e}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            raise

    asyncio.run(main())
