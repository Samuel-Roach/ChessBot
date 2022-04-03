from enum import Enum
from dataclasses import dataclass

class PieceColor(Enum):
    """ Enum representation of a Chess Piece's Color """
    WHITE = 0
    BLACK = 1
    NEUTRAL = 2


class PieceType(Enum):
    """ Enum representation of a Chess Piece's Type """
    PAWN = 0
    KNIGHT = 1
    BISHOP = 2
    ROOK = 3
    QUEEN = 4
    KING = 5


@dataclass
class ChessPiece:
    """ Representation of a Chess Piece """
    color: PieceColor
    piece_type: PieceType
    moves: int

    def __init__(self, color: PieceColor, piece_type: PieceType) -> None:
        self.color = color
        self.piece_type = piece_type
        self.moves = 0
        pass