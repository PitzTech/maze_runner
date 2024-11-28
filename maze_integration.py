import asyncio
from labirinto import Labirinto
from agente_explorador import AgenteExplorador
from websocket_maze_client import WebSocketMazeSolver
from config import load_maze_config

class MazeIntegration:
    def __init__(self):
        self.config = load_maze_config()
        self.solver = WebSocketMazeSolver(self.config)

    async def solve(self):
        min_path = await self.solver.explore()
        return min_path

def main():
    try:
        # Run local maze solver
        # labirinto = Labirinto(11, 11)
        # agente = AgenteExplorador(labirinto)
        # agente.explorar()

        # Run WebSocket maze solver
        integration = MazeIntegration()
        ws_min_path = asyncio.run(integration.solve())
        print(f"WebSocket maze solution path: {ws_min_path}")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
