from typing import Tuple
from src.chess_piece import ChessPiece, PieceColor, PieceType
from dataclasses import dataclass

@dataclass
class ChessMove:
    # About the move
    piece: ChessPiece
    move_notation: str
    current_location: tuple
    next_location: tuple

    # Additional information
    capture: ChessPiece
    check: bool
    checkmate: bool
    castling: bool


class MoveParser:
    """ Parser to take a string value and return a ChessMove"""

    # def check_valid_move(self, current_board, start_position: tuple(int, int), end_position: tuple(int, int)):
    #     piece_to_move = current_board[start_position[0]][start_position[1]]

    def _str_to_tuple(self, string: str):
        """ Convert a string representation of a chess move into the tuple representation """
        string_components = list((string[0], string[1]))
        coord1, coord2 = int(ord(string_components[0].upper()) - 64), int(string_components[1])
        if all([coord1 > 0, coord1 < 9, coord2 > 0, coord2 < 9]):
            return (coord1, coord2) 
        else:
            raise Exception(f"Invalid move coords: {coord1}, {coord2}")

    def convert_start_end(self, start: str, end: str):
        """ Take the start and end positions and return their tuple(int, int) representation """
        return self._str_to_tuple(start), self._str_to_tuple(end)


    def parse_move(self, start: str, end: str, current_board: list):
        """ Parse a move defined by a start and end (e.g. a3, a4) and turn it into a ChessMove type """
        start_move, end_move = self.convert_start_end(start, end)
        print(start_move)
        print(end_move)

        # Parse strings into locations
        # Check the locations are valid
        # Check the move is valid for the piece that's moving
        # Check if a piece is being taken
        # Check if castling is taking place
        # Check if check/mate