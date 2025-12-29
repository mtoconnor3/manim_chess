from manim import *
import numpy as np

class ManimPiece(Group):
    def __init__(self, piece: ch.Piece, square: int):
        super().__init__()
        self.piece = piece
        self.square = square
        self.mob = self.load_svg(piece)
        self.add(self.mob)
        self.move_to_square(square)

    def load_svg(self, piece):
        file = f"assets/{piece.symbol()}.svg"
        return SVGMobject(file).scale(0.8)

    def move_to_square(self, square):
        self.square = square
        pos = np.array([square % 8 - 3.5, 3.5 - square//8, 0])
        self.move_to(pos)

    def animate_move(self, target_square):
        return self.animate.move_to_square(target_square)
