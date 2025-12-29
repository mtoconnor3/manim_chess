import chess as ch
from manim import *

class ManimBoard(ch.Board):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.manim_board = None
        self.piece_mobs = {}

    def build_board(self):
        squares = VGroup()
        colors = [WHITE, GREY]  # don't lock colors too early
        for i in range(64):
            sq = Square(side_length=1)
            sq.set_fill(colors[(i + i//8) % 2], opacity=1)
            sq.set_stroke(BLACK, width=1)
            sq.move_to([i % 8 - 3.5, 3.5 - i//8, 0])
            squares.add(sq)
        self.manim_board = squares
        return self.manim_board

    def add_pieces(self):
        for square, piece in self.piece_map().items():
            mob = ManimPiece(piece, square)
            self.piece_mobs[square] = mob
            self.piece_mobs[ch.square_name(square)] = mob