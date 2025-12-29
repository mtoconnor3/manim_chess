from manim import *
from manim_board import *
import chess as ch

from chess.pgn import read_game

class ChessScene(Scene):
    def construct(self):
        pgn_path = "assets/morphy_opera_game.pgn"
        game = self.fetch_pgn(pgn_path)
        
        board = ManimBoard()
        self.add(board.board_mob)
        for mob in board.piece_mobs.values():
            self.add(mob)

        for move in game.mainline_moves():
            animations = board.push(move)
            if animations:
                self.play(*animations, run_time=0.3)
            self.wait(1)
        self.wait(2)

    def fetch_pgn(self, pgn_path: str): 
        with open(pgn_path, "r") as f:
            game = read_game(f)

        return game