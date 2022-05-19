from typing import Tuple
from src.chess_piece import ChessPiece, PieceColor, PieceType
from constants.transform_constants import PIECE_TRANSFORMS
from dataclasses import dataclass
from copy import deepcopy

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
    stalemate: bool
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


    def _get_threat_matrix_on_board(self, piece_color: PieceColor, board: list) -> list:
        """ Get the list of squares that a color is threatening on a board """
        threat_matrix = []

        for x in range(0, 8):
            for y in range(0, 8):
                piece : ChessPiece = board[y][x]
                if (piece != None) and (piece.color == piece_color):
                    # Loop over the pieces possibles positions checking if they're in check
                    # Add defended positions too
                    piece_transforms = PIECE_TRANSFORMS[piece.piece_type]
                    color_transforms = PieceColor.NEUTRAL if PieceColor.NEUTRAL in piece_transforms else piece.color
                    
                    for transform in piece_transforms[color_transforms]:
                        direction_x = transform[0]
                        direction_y = transform[1]
                        direction_mag = transform[2]

                        for mag in range(1, direction_mag):
                            if (y + (direction_y * mag) > 7 or y + (direction_y * mag) < 0 or x + (direction_x * mag) > 7 or x + (direction_x * mag) < 0):
                                break

                            checking_location : ChessPiece = board[y + (direction_y * mag)][x + (direction_x * mag)]
                            if checking_location == None:
                                threat_matrix.append((x + (direction_x * mag), y + (direction_y * mag)))
                            elif checking_location.color == piece.color:
                                threat_matrix.append((x + (direction_x * mag), y + (direction_y * mag)))
                                break
                            elif checking_location.color != piece_color:
                                threat_matrix.append((x + (direction_x * mag), y + (direction_y * mag)))
                                break
                            else:
                                break

        return threat_matrix


    def _get_threat_matrix(self, piece_color: PieceColor) -> list:
        """ Get the list of squares that a color is threatening """
        return self._get_threat_matrix_on_board(piece_color, self.current_board)


    def _color_in_check_on_board(self, piece_color: PieceColor, board: list) -> bool:
        """ Check if a color is in check on a certain board """

        # for every position on the board
            # if the piece is opposite to piece_color
                # check the possible locations for if the piece_color.king is there
                # if so, color is in check
        # https://gist.github.com/pingpoli/1d7e0d4cef2090fd1e396bd4c60c70bd
        king_location = ()

        for x in range(0, 8):
            for y in range(0, 8):
                piece : ChessPiece = board[y][x]
                if piece == None: continue
                if (piece.piece_type == PieceType.KING and piece.color == piece_color):
                    king_location = (x, y)


        threat_color = PieceColor.WHITE if piece_color == PieceColor.BLACK else PieceColor.BLACK

        return king_location in self._get_threat_matrix(threat_color)


    def _color_in_check(self, piece_color: PieceColor) -> bool:
        """ Check if a color is in check """
        return self._color_in_check_on_board(piece_color, self.current_board)


    def _color_in_checkmate(self, piece_color: PieceColor):
        """ Check if a color has been checkmated """

        for x in range(0, 8):
            for y in range(0, 8):
                piece : ChessPiece = self.current_board[y][x]
                if piece != None and piece.color == piece_color:
                    piece_transforms = PIECE_TRANSFORMS[piece.piece_type]
                    color_transforms = PieceColor.NEUTRAL if PieceColor.NEUTRAL in piece_transforms else piece.color

                    for transform in piece_transforms[color_transforms]:
                        direction_x = transform[0]
                        direction_y = transform[1]
                        direction_mag = transform[2]

                        for mag in range(direction_mag):
                            mag += 1
                            if (y + (direction_y * mag) > 7 or y + (direction_y * mag) < 0 or x + (direction_x * mag) > 7 or x + (direction_x * mag) < 0):
                                break

                            checking_location : ChessPiece = self.current_board[y + (direction_y * mag)][x + (direction_x * mag)]
                            if checking_location == None:
                                # Create a new board with the current piece in the checking_location
                                # If the new board has !color_in_check of piece_color then we know that
                                # the piece_color isn't in checkmate
                                new_board = deepcopy(self.current_board)
                                new_board[x][y] = None
                                new_board[x + (direction_x * mag)][y + (direction_y * mag)] = piece
                                if not self._color_in_check_on_board(piece_color, new_board):
                                    return False
                            elif checking_location.color == piece.color:
                                break
                            elif checking_location.color != piece_color:
                                # Create a new board with the current piece in the checking_location
                                # If the new board has !color_in_check of piece_color then we know that
                                # the piece_color isn't in checkmate
                                new_board = deepcopy(self.current_board)
                                new_board[x][y] = None
                                new_board[x + (direction_x * mag)][y + (direction_y * mag)] = piece
                                if not self._color_in_check_on_board(piece_color, new_board):
                                    return False
                                break
                            else:
                                break
        return True

    def _color_in_stalemate(self, piece_color: PieceColor) -> bool:
        """ Return if a color has been stalemated or not """
        can_move = False

        for x in range(0, 8):
            for y in range(0, 8):
                piece : ChessPiece = self.current_board[y][x]
                if piece != None and piece.color == piece_color:
                    piece_transforms = PIECE_TRANSFORMS[piece.piece_type]
                    color_transforms = PieceColor.NEUTRAL if PieceColor.NEUTRAL in piece_transforms else piece.color

                    for transform in piece_transforms[color_transforms]:
                        direction_x = transform[0]
                        direction_y = transform[1]
                        direction_mag = transform[2]

                        for mag in range(direction_mag):
                            mag += 1
                            y_checking = y + (direction_y * mag)
                            x_checking = x + (direction_x * mag)

                            if (y_checking > 7 or y_checking < 0 or x_checking > 7 or x_checking < 0):
                                break

                            checking_location : ChessPiece = self.current_board[y_checking][x_checking]
                            if checking_location == None:
                                # Check if moving this piece results in a check
                                # If not, this is not a stalemate
                                new_board = deepcopy(self.current_board)
                                new_board[x][y] = None
                                new_board[x + (direction_x * mag)][y + (direction_y * mag)] = piece
                                if not self._color_in_check_on_board(piece_color, new_board):
                                    can_move = True
                                    return (not can_move)
                                break
                            elif checking_location.color == piece.color:
                                break
                            elif checking_location.color != piece_color:
                                # Check if taking this piece doesn't result in check
                                # If so, this isn't a stalemate
                                new_board = deepcopy(self.current_board)
                                new_board[x][y] = None
                                new_board[x + (direction_x * mag)][y + (direction_y * mag)] = piece
                                if not self._color_in_check_on_board(piece_color, new_board):
                                    can_move = True
                                    return (not can_move)
                                break
                            else:
                                break

        return (not can_move)

    def possible_move(self):
        """ Check if the current move defined is a possible move """
        end_piece = self.current_board[self.current_move.end_move[1]][self.current_move.end_move[0]]

        # Check you're not landing on your own piece
        if end_piece and (end_piece.color == self.current_move.piece.color):
            return False
        elif end_piece:
            self.current_move.capture = end_piece

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

        enemy_color = PieceColor.BLACK if move.piece.color == PieceColor.WHITE else PieceColor.WHITE

        if self._color_in_check(move.piece.color):
            raise Exception("You can't move into check")

        if self._color_in_check(enemy_color):
            move.check = True

            if (self._color_in_checkmate(enemy_color)):
                move.checkmate = True
        else:
            if (self._color_in_stalemate(enemy_color)):
                move.stalemate = True


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
            stalemate=False,
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