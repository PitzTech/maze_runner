from typing import NamedTuple
import os
from dotenv import load_dotenv

class MazeConfig(NamedTuple):
    grupo_id: str
    labirinto_id: str
    websocket_url: str

def load_maze_config() -> MazeConfig:
    load_dotenv()

    grupo_id = os.getenv('MAZE_GRUPO_ID')
    labirinto_id = os.getenv('MAZE_LABIRINTO_ID')
    websocket_url = os.getenv('MAZE_WEBSOCKET_URL')

    missing = []
    if not grupo_id: missing.append('MAZE_GRUPO_ID')
    if not labirinto_id: missing.append('MAZE_LABIRINTO_ID')
    if not websocket_url: missing.append('MAZE_WEBSOCKET_URL')

    if missing:
        raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

    return MazeConfig(grupo_id, labirinto_id, websocket_url)
