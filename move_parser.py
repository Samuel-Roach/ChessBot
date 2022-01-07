from chess_piece import ChessPiece, PieceColor, PieceType
from dataclasses import dataclass

@dataclass
class ChessMove:
    # About the move
    piece: ChessPiece
    move_notation: str
    current_location: tuple(int, int)
    next_location: tuple(int, int)

    # Additional information
    capture: ChessPiece
    check: bool
    checkmate: bool
    castling: bool


class MoveParser:
    """ Parser to take a string value and return a ChessMove"""

    def check_valid_move(self, current_board, start_position: tuple(int, int), end_position: tuple(int, int)):
        piece_to_move = current_board[start_position[0]][start_position[1]]