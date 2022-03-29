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


    def _str_to_tuple(self, string: str):
        """ Convert a string representation of a chess move into the tuple representation """

        string_components = list((string[0], string[1]))
        coord1, coord2 = int(ord(string_components[0].upper()) - 64), int(string_components[1])
        if all([coord1 > 0, coord1 < 9, coord2 > 0, coord2 < 9]):
            return (coord1 - 1, coord2 - 1) 
        else:
            raise Exception(f"Invalid move coords: {coord1}, {coord2}")


    def _custom_range(self, start, end):
        """ Return custom range function calls depending on which input is larger """

        if (start > end):
            return range(start, end, -1)
        else:
            return range(start, end)


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
                return self.valid_move_pawn()
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
        """ Evaluate if a pawn move is valid """

        # TODO Get the rest of the valid pawn moves working
        # Black/White distinction
        # Taking another piece
        # En passant

        x_change = abs(self.current_move.end_move[0] - self.current_move.start_move[0])
        y_change = abs(self.current_move.end_move[1] - self.current_move.start_move[1])

        if (self.current_move.piece.moves == 0):
            return (x_change == 0) and (y_change in (1,2))
        else:
            return (x_change == 0) and (y_change == 1)

    def valid_move_knight(self):
        """ Evaluate if a knight move is valid """

        x_change = abs(self.current_move.end_move[0] - self.current_move.start_move[0])
        y_change = abs(self.current_move.end_move[1] - self.current_move.start_move[1])

        return (x_change == 2 and y_change == 1) or (x_change == 1 and y_change == 2)


    def valid_move_bishop(self):
        """ Evaluate if a bishop move is valid """

        x_change = abs(self.current_move.end_move[0] - self.current_move.start_move[0])
        y_change = abs(self.current_move.end_move[1] - self.current_move.start_move[1])

        if (x_change == y_change):
            start = self.current_move.start_move
            end = self.current_move.end_move
            for x, y in zip(self._custom_range(start[0], end[0]), self._custom_range(start[1], end[1])):
                if (x == self.current_move.end_move[0]) and self.current_move.capture != None:
                    return True

                if self.current_board[y][x] not in [None, self.current_move.piece]:
                    return False

            return True
        else:
            return False


    def valid_move_rook(self):
        """ Evaluate if a rook move is valid """

        x_change = abs(self.current_move.end_move[0] - self.current_move.start_move[0])
        y_change = abs(self.current_move.end_move[1] - self.current_move.start_move[1])

        # X axis movement, check nothing's in the way
        if x_change != 0 and y_change == 0:
            for x in self._custom_range(self.current_move.start_move[0], self.current_move.end_move[0]):
                if (x == self.current_move.end_move[0]) and self.current_move.capture != None:

                    return True

                if self.current_board[self.current_move.start_move[1]][x] not in [None, self.current_move.piece]:
                    return False

            return True

        # Y axis movement, check nothing's in the way
        elif x_change == 0 and y_change != 0:
            for y in self._custom_range(self.current_move.start_move[1], self.current_move.end_move[1]):
                if (y == self.current_move.end_move[0]) and self.current_move.capture != None:
                    return True

                if self.current_board[y][self.current_move.start_move[0]] not in [None, self.current_move.piece]:
                    print("Can't move")
                    print(f"{self.current_move.piece}")
                    print(f"{self.current_board[y][self.current_move.start_move[0]]}")
                    return False

            return True

        else:
            return False


    def valid_move_queen(self):
        """ Evaluate if a queen move is valid """

        return self.valid_move_rook() or self.valid_move_bishop()


    def valid_move_king(self):
        """ Evaluate if a king move is valid """

        # TODO Get castling working

        x_change = abs(self.current_move.end_move[0] - self.current_move.start_move[0])
        y_change = abs(self.current_move.end_move[1] - self.current_move.start_move[1])

        return (x_change <= 1) and (y_change <= 1)


    def make_move(self):
        self.current_board[self.current_move.end_move[1]][self.current_move.end_move[0]] = self.current_move.piece
        self.current_board[self.current_move.start_move[1]][self.current_move.start_move[0]] = None


    def parse_move(self, start: str, end: str, current_board: list, to_move: PieceColor):
        """ Parse a move defined by a start and end (e.g. a3, a4) and turn it into a ChessMove type """

        self.current_board = current_board

        start_move, end_move = self.convert_start_end(start, end)
        self.current_move = ChessMove(
            piece=current_board[start_move[1]][start_move[0]],
            move_notation="",
            start_move=start_move,
            end_move=end_move,
            capture=None,
            check=False,
            checkmate=False,
            castling=False,
            en_passant=False
        )

        if self.current_move.piece.color != to_move:
            raise Exception("You can't move that color pieces")

        if self.possible_move():
            self.current_move.piece.moves += 1
            self.make_move()
        else:
            raise Exception("Invalid move attempted")

        # Parse strings into locations
        # Check the locations are valid
        # Check the move is valid for the piece that's moving
        # Check if a piece is being taken
        # Check if castling is taking place
        # Check if check/mate
        # Check for en passant
        # Check the user can make that move