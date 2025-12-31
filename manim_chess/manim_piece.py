from manim import *
import numpy as np
import chess as ch

class ManimPiece(Group):
    def __init__(self, piece: ch.Piece, square: int):
        super().__init__()
        self.piece = piece
        self.square = square
        self.mob = self.load_svg(piece)
        self.add(self.mob)
        self.move_to_square(square)

    def load_svg(self, piece: ch.Piece):
        mob = SVGMobject(f"assets/{piece.symbol().lower()}.svg").scale(0.4)

        if piece.color == ch.WHITE:
            mob.set_fill(WHITE, opacity=1)
            mob.set_stroke(BLACK, width=2)  # outline for white pieces
        else:
            mob.set_fill(BLACK, opacity=1)

        return mob

    def move_to_square(self, square):
        self.square = square
        pos = np.array([square % 8 - 3.5, square//8 - 3.5, 0])
        self.move_to(pos)

    def animate_move(self, target_square):
        return self.animate.move_to_square(target_square)

    def animate_capture(self):
        return FadeOut(self)
    
    def promote_to(self, new_piece: ch.Piece):
        self.piece = new_piece
        new_graphic = self.load_svg(new_piece)
        self.remove(self.graphic)
        self.graphic = new_graphic
        self.add(self.graphic)