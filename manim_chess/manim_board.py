import chess as ch
from manim import *

from manim_piece import ManimPiece
from utils import square_to_coords

class ManimBoard(ch.Board):
    def __init__(self):
        super().__init__()
        self.square_size = 1
        self.board_mob = self._build_board()
        self.piece_mobs = self._create_piece_mobs()

    def _build_board(self):
        grid = VGroup()
        for sq in range(64):
            file = sq % 8
            rank = sq // 8
            # Bottom-left a1 = GREY
            color = GREY if (file + rank) % 2 == 0 else WHITE
            square = Square(side_length=self.square_size)
            square.set_fill(color, opacity=1)
            square.set_stroke(BLACK, width=1)
            # Map a1 to bottom-left in Manim coordinates
            square.move_to(square_to_coords(sq))
            grid.add(square)
        return grid

    def _create_piece_mobs(self):
        mobs = {}
        for square, piece in self.piece_map().items():
            mob = ManimPiece(piece, square)
            mobs[square] = mob
        return mobs
    
    def push(self, move: ch.Move):
        animations = []

        from_sq = move.from_square
        to_sq = move.to_square
        piece = self.piece_mobs.get(from_sq)

        # 1. Handle captures
        if self.is_capture(move):
            if to_sq in self.piece_mobs:
                captured = self.piece_mobs[to_sq]
                animations.append(captured.animate_capture())
                # mark for removal after animation
                captured.removed = True

        # 2. Handle castling
        if piece.piece.piece_type == ch.KING and ch.square_file(to_sq) - ch.square_file(from_sq) in (2, -2):
            rook_from, rook_to = self._get_castling_rook_squares(move)
            rook = self.piece_mobs.get(rook_from)
            if rook:
                animations.append(rook.animate_move(rook_to))
                self.piece_mobs[rook_to] = rook
                del self.piece_mobs[rook_from]

        # 3. En-passant capture
        if move in self.generate_legal_moves() and self.ep_square and to_sq == self.ep_square:
            ep_victim_sq = self._get_en_passant_victim_square(move)
            victim = self.piece_mobs.get(ep_victim_sq)
            if victim:
                animations.append(victim.animate_capture())
                victim.removed = True
                del self.piece_mobs[ep_victim_sq]

        # 4. Animate moving piece
        if piece:
            animations.append(piece.animate_move(to_sq))

        # Push move in python-chess logic
        super().push(move)

        # 5. Handle promotion swap
        if move.promotion:
            piece.promote_to(ch.Piece(move.promotion, piece.piece.color))

        # 6. Re-key moved piece
        if piece:
            self.piece_mobs[to_sq] = piece
            del self.piece_mobs[from_sq]

        # 7. Remove captured pieces from dict after animation
        self.piece_mobs = {sq: mob for sq, mob in self.piece_mobs.items() if not getattr(mob, "removed", False)}

        return animations
    
    def _get_castling_rook_squares(self, move):
        if self.turn == ch.WHITE:
            return (ch.H1, ch.F1) if move.to_square > move.from_square else (ch.A1, ch.D1)
        else:
            return (ch.H8, ch.F8) if move.to_square > move.from_square else (ch.A8, ch.D8)
    
    def _get_en_passant_victim_square(self, move):
        direction = -8 if self.turn == ch.WHITE else 8
        return move.to_square + direction