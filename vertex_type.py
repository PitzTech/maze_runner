from enum import Enum

class VertexType(Enum):
    """
    Enumeration for vertex types in the maze.

    Values:
    - NORMAL (0): Regular vertex
    - ENTRADA (1): Entry point
    - SAIDA (2): Exit point
    """
    NORMAL = "0"
    ENTRADA = "1"
    SAIDA = "2"

    @classmethod
    def from_value(cls, value: str) -> "VertexType":
        """
        Creates a VertexType from a string value.
        Handles both numeric and string representations.
        """
        # Map string representations to enum values
        value_map = {
            "0": cls.NORMAL,
            "1": cls.ENTRADA,
            "2": cls.SAIDA,
            "normal": cls.NORMAL,
            "entrada": cls.ENTRADA,
            "saida": cls.SAIDA
        }

        try:
            return value_map[str(value).lower()]
        except KeyError:
            raise ValueError(f"Invalid vertex type: {value}")

    def __str__(self) -> str:
        return self.value
