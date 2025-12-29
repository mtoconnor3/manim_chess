import numpy as np

def square_to_coords(square: int) -> np.ndarray:
    """
    Maps python-chess square index (0=a1..63=h8) to Manim coordinates.
    """
    file = square % 8
    rank = square // 8
    y = rank - 3.5
    x = file - 3.5
    return np.array([x, y, 0])