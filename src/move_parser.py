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
            return (coord1 - 1, coord2 - 1) 
        else:
            raise Exception(f"Invalid move coords: {coord1}, {coord2}")

    def convert_start_end(self, start: str, end: str):
        """ Take the start and end positions and return their tuple(int, int) representation """
        return self._str_to_tuple(start), self._str_to_tuple(end)

    def possible_moves(self, piece: ChessPiece, position: tuple):
        """ Generate the possible moves for a ChessPiece on a given square """
        possible_moves = []

        match piece.piece_type:
            case PieceType.PAWN:
                print("PAWN")
            case PieceType.KNIGHT:
                possible_moves = self.possible_moves_knight(position)
            case PieceType.BISHOP:
                possible_moves = self.possible_moves_bishop(position)
            case PieceType.ROOK:
                possible_moves = self.possible_moves_rook(position)
            case PieceType.QUEEN:
                possible_moves = self.possible_moves_queen(position)
            case PieceType.KING:
                possible_moves = self.possible_moves_king(position)

        self._remove_impossible_positions(possible_moves, position)

        return possible_moves


    # def possible_moves_pawn(self, ):


    def possible_moves_knight(self, position: tuple):
        """ Return the possible moves for a knight at the given position """
        possible_moves = []

        possible_changes = [
            (2, 1),
            (2, -1),
            (-2, 1),
            (-2, -1),
            (1, 2),
            (1, -2),
            (-2, 2),
            (-2, -2)
        ]

        for change in possible_changes:
            possible_moves.append((position[0] + change[0], position[1] + change[1]))

        return possible_moves


    def possible_moves_bishop(self, position: tuple):
        """ Return the possible moves for a bishop at the given position """
        possible_moves = []

        self._add_diagonals(possible_moves, position)

        return possible_moves


    def possible_moves_rook(self, position: tuple):
        """ Return the possible moves for a rook at the given position """
        possible_moves = []

        self._add_perpendiculars(possible_moves, position)

        return possible_moves


    def possible_moves_queen(self, position: tuple):
        """ Return the possible moves for a queen at the given position """
        possible_moves = []

        self._add_diagonals(possible_moves, position)
        self._add_perpendiculars(possible_moves, position)

        return possible_moves


    def possible_moves_king(self, position: tuple):
        """ Return the possible moves for a king at the given position """
        possible_moves = []

        self._add_diagonals(possible_moves, position, 1)
        self._add_perpendiculars(possible_moves, position, 1)

        return possible_moves


    def _add_diagonals(self, positions: list, current_position: tuple, size: int = 7):
        """ Add the possible diagonal positions to a list of possible positions """
        for x_change in range(-size, size):
            x_pos = (current_position[0] + x_change)
            positions.append((x_pos, current_position[1] + x_change))
            positions.append((x_pos, current_position[1] - x_change))


    def _add_perpendiculars(self, positions: list, current_position: tuple, size: int = 7):
        """ Add the possible perpendicular positions to a list of possible positions """
        for x_change in range(-size, size):
            x_pos = (current_position[0] + x_change)
            positions.append((x_pos, current_position[1]))

        for y_change in range(-size, size):
            y_pos = (current_position[1] + y_change)
            positions.append((current_position[0], y_pos))


    def _remove_impossible_positions(self, positions: list, current_position: tuple):
        """ Remove the impossible positions from a list of possible piece positions """
        for possible_move in positions:
            if ((possible_move[0] not in range(0,7)) and (possible_move[1] not in range(0,7))):
                positions.remove(possible_move)

            if (possible_move[0] == current_position[0] and possible_move[1] == current_position[1]):
                positions.remove(possible_move)


    def parse_move(self, start: str, end: str, current_board: list):
        """ Parse a move defined by a start and end (e.g. a3, a4) and turn it into a ChessMove type """
        start_move, end_move = self.convert_start_end(start, end)
        piece_to_move = current_board[start_move[1]][start_move[0]]
        possible_moves = self.possible_moves(piece_to_move, start_move)
        print(start_move)
        print(end_move)
        print(piece_to_move.piece_type)

        # Parse strings into locations
        # Check the locations are valid
        # Check the move is valid for the piece that's moving
        # Check if a piece is being taken
        # Check if castling is taking place
        # Check if check/mate
        # Check for en passant
        # Check the user can make that move