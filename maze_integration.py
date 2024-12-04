import asyncio
from labirinto import Labirinto
from agente_explorador import AgenteExplorador
from websocket_maze_client import WebSocketMazeSolver
from config import load_maze_config
import traceback

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
        traceback.print_exc()
    except Exception as e:
        print(f"Unexpected error: {e}")
        print("\nFull traceback:")
        traceback.print_exc()  # This will print the full stack trace

        # Additional debug info
        if hasattr(e, '__traceback__'):
            tb = traceback.extract_tb(e.__traceback__)
            print("\nError occurred in:")
            for filename, line, func, text in tb:
                print(f"File: {filename}, Line {line}")
                print(f"Function: {func}")
                print(f"Code: {text}\n")

if __name__ == "__main__":
    main()
