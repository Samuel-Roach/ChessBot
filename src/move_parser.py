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
    previous_move: ChessMove


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


    def _en_passant_check(self):
        """ Check if the current move is en passant """
        y_diff = 1 if self.current_move.piece.color == PieceColor.WHITE else -1

        if (
            self.previous_move.piece.moves == 1 and
            abs(self.previous_move.start_move[1] - self.previous_move.end_move[1]) == 2 and
            (self.current_move.end_move[1] - self.previous_move.end_move[1]) == y_diff
           ):
            self.current_move.en_passant = True
            return True
        else:
            return False


    def _castling_check(self, x_change: int):
        """ Check if the current move is castling """
        if (abs(x_change) != 2):
            return False
        
        if (x_change == 2):
            moving_rook = self.current_board[self.current_move.start_move[1]][7]
            pieces_between = [self.current_board[self.current_move.start_move[1]][5], self.current_board[self.current_move.start_move[1]][6]]
            if (
                moving_rook.moves == 0 and
                all(piece == None for piece in pieces_between) and
                self.current_move.piece.moves == 0
               ):
                self.current_move.castling = True
                return True

        if (x_change == -2):
            moving_rook = self.current_board[self.current_move.start_move[1]][0]
            pieces_between = [self.current_board[self.current_move.start_move[1]][1], self.current_board[self.current_move.start_move[1]][2], self.current_board[self.current_move.start_move[1]][3]]
            if (
                moving_rook.moves == 0 and
                all(piece == None for piece in pieces_between) and
                self.current_move.piece.moves == 0
               ):
                self.current_move.castling = True
                return True

        return False


    def _color_in_check(self, piece_color: PieceColor):
        """ Check if a color is in check """

        # TODO List of all places a e.g. white piece could move to
        # TODO All white pieces defended by another white piece
        # for every position on the board
            # if the piece is opposite to piece_color
                # check the possible locations for if the piece_color.king is there
                # if so, color is in check
        # https://gist.github.com/pingpoli/1d7e0d4cef2090fd1e396bd4c60c70bd
        return list


    def possible_move(self):
        """ Check if the current move defined is a possible move """
        end_piece = self.current_board[self.current_move.end_move[1]][self.current_move.end_move[0]]

        # Check you're not landing on your own piece
        if end_piece and (end_piece.color == self.current_move.piece.color):
            return False
        elif end_piece:
            self.current_move.capture = end_piece

        #TODO add check for if you're in check, protect the check
        #TODO Check that you're not moving into check
        #TODO add a check to mark a move as making a check

        return_value = False

        match self.current_move.piece.piece_type:
            case PieceType.PAWN:
                return_value = self.valid_move_pawn()
            case PieceType.KNIGHT:
                return_value = self.valid_move_knight()
            case PieceType.BISHOP:
                return_value = self.valid_move_bishop()
            case PieceType.ROOK:
                return_value = self.valid_move_rook()
            case PieceType.QUEEN:
                return_value = self.valid_move_queen()
            case PieceType.KING:
                return_value = self.valid_move_king()

        # TODO Check whether check has been made
        # TODO For check we need to use a Threat map https://levelup.gitconnected.com/finding-all-legal-chess-moves-2cb872d05bc6

        check_color = PieceColor.BLACK if self.current_move.piece.color == PieceColor.WHITE else PieceColor.BLACK
        if self._color_in_check(check_color):
            self.current_move.check = True

        return return_value


    def valid_move_pawn(self):
        """ Evaluate if a pawn move is valid """
        x_change = self.current_move.end_move[0] - self.current_move.start_move[0]
        y_change = self.current_move.end_move[1] - self.current_move.start_move[1]

        y_direction = 1 if (self.current_move.piece.color == PieceColor.WHITE) else -1

        if x_change in (1, -1):
            return (
                (self.current_move.capture != None) and (self.current_move.capture.color != self.current_move.piece.color) or
                self._en_passant_check()
            )
        
        if (self.current_move.piece.moves == 0):
            return (x_change == 0) and (y_change in (1 * y_direction, 2 * y_direction))
        else:
            return (x_change == 0) and (y_change == (1 * y_direction))

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
        x_change = self.current_move.end_move[0] - self.current_move.start_move[0]
        y_change = abs(self.current_move.end_move[1] - self.current_move.start_move[1])

        return ((abs(x_change) <= 1) and (y_change <= 1)) or (self._castling_check(x_change) and y_change == 0)


    def make_move(self, board: list, move: ChessMove):
        """ Make a Chess move on a given board """
        board[move.end_move[1]][move.end_move[0]] = move.piece
        board[move.start_move[1]][move.start_move[0]] = None

        # En passant check
        if (move.en_passant):
            y_diff = -1 if move.piece.color == PieceColor.WHITE else 1

            remove_y = move.end_move[1] + y_diff
            board[remove_y][move.end_move[0]] = None

        # Castling check
        if (move.castling):
            if move.start_move[0] > move.end_move[0]:
                rook_pos = (0, move.start_move[1])
                rook = board[rook_pos[1]][rook_pos[0]]

                board[rook_pos[1]][3] = rook
                rook.moves += 1
                board[rook_pos[1]][rook_pos[0]] = None
            else:
                rook_pos = (7, move.start_move[1])
                rook = board[rook_pos[1]][rook_pos[0]]

                board[rook_pos[1]][5] = rook
                rook.moves += 1
                board[rook_pos[1]][rook_pos[0]] = None



    def parse_move(self, start: str, end: str, current_board: list, to_move: PieceColor, previous_move: ChessMove):
        """ Parse a move defined by a start and end (e.g. a3, a4) and turn it into a ChessMove type """
        self.current_board = current_board
        self.previous_move = previous_move

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
            return self.current_move
        else:
            raise Exception("Invalid move attempted")

        # Check if check/mate