from manim import *
from manim_board import *

class ChessScene(Scene):
    def construct(self):
        board = ManimBoard()
        grid = board.build_board()
        self.add(grid)

        board.add_pieces()
        for piece in board.piece_mobs.values():
            self.add(piece)

        move = ch.Move.from_uci("e2e4")
        if move in board.legal_moves:
            anim = board.piece_mobs[move.from_square].animate_move(move.to_square)
            self.play(anim)
            board.push(move)
