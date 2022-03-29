from typing import Tuple
from src.chess_piece import ChessPiece, PieceColor, PieceType
from dataclasses import dataclass

@dataclass
class ChessMove:
    # About the move
    piece: ChessPiece
    move_notation: str
    start_move: tuple
    end_move: tuple

    # Additional information
    capture: ChessPiece
    check: bool
    checkmate: bool
    castling: bool
    en_passant: bool


class MoveParser:
    """ Parser to take a string value and return a ChessMove"""
    current_board: list
    current_move: ChessMove


    def __init__(self) -> None:
        pass


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


    def possible_move(self):
        """ Check if the current move defined is a possible move """
        end_piece = self.current_board[self.current_move.end_move[1]][self.current_move.end_move[0]]

        if end_piece and (end_piece.color == self.current_move.piece.color):
            return False
        else:
            self.current_move.capture = end_piece

        match self.current_move.piece.piece_type:
            case PieceType.PAWN:
                print("PAWN check")
            case PieceType.KNIGHT:
                return self.valid_move_knight()
            case PieceType.BISHOP:
                return self.valid_move_bishop()
            case PieceType.ROOK:
                return self.valid_move_rook()
            case PieceType.QUEEN:
                return self.valid_move_queen()
            case PieceType.KING:
                return self.valid_move_king()


    def valid_move_pawn(self):
        return False

    def valid_move_knight(self):
        """ Evaluate if a knight move is valid """

        x_change = abs(self.current_move.end_move[0] - self.current_move.start_move[0])
        y_change = abs(self.current_move.end_move[1] - self.current_move.start_move[1])

        return (x_change == 2 and y_change == 1) or (x_change == 1 and y_change == 2)


    def valid_move_bishop(self):
        """ Evaluate if a bishop move is valid """

        return False


    def valid_move_rook(self):
        """ Evaluate if a rook move is valid """

        if (self.current_move.start_move[0] != self.current_move.end_move[0]) or (self.current_move.start_move[1] != self.current_move.end_move[1]):
            return False

        if self.current_move.start_move[0] == self.current_move.end_move[0]:
            x = self.current_move.start_move[0]
            for y in range(self.current_move.start_move[1], self.current_move.end_move[1]):
                if (self.current_move.capture != None) and (y == self.current_move.end_move[1]):
                    return True

                if self.current_board[y][x] != None:
                    return False

            return True
        return False


    def valid_move_queen(self):
        """ Evaluate if a queen move is valid """

        return False


    def valid_move_king(self):
        """ Evaluate if a king move is valid """

        return False


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
        self.current_board = current_board

        start_move, end_move = self.convert_start_end(start, end)
        self.current_move = ChessMove(
            piece=current_board[start_move[1]][start_move[0]],
            start_move=start_move,
            end_move=end_move,
            capture=None,
            check=False,
            checkmate=False,
            castling=False,
            en_passant=False
        )

        possible_moves = self.possible_move()
        print(f"Start {self.start_move}")
        print(f"End   {self.end_move}")
        print(f"Piece {self.piece.piece_type}")
        print(possible_moves)

        # Parse strings into locations
        # Check the locations are valid
        # Check the move is valid for the piece that's moving
        # Check if a piece is being taken
        # Check if castling is taking place
        # Check if check/mate
        # Check for en passant
        # Check the user can make that move