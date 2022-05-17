import constants.game_constants as game_constants

from src.game_renderer import ChessRenderer
from src.move_parser import ChessMove, MoveParser
from src.chess_piece import PieceColor

from copy import deepcopy

class ChessGameEngine:
    """ Engine playing a game of chess """

    renderer = ChessRenderer()
    move_parser = MoveParser()


    def __init__(self, move_list=None, board=None, to_move=None, winner_color=None) -> None:
        # Create the basic board
        if move_list == None:
            self.move_list = [None]
        else:
            self.move_list = move_list

        if board == None:
            self.board = deepcopy(game_constants.DEFAULT_BOARD)
        else:
            self.board = board

        if to_move == None:
            self.to_move = PieceColor.WHITE
        else:
            self.to_move = to_move

        if winner_color == None:
            self.winner_color = None
        else:
            self.winner_color = winner_color
        pass


    # Move
    def move(self, start: str, end: str) -> bool:
        """ Move a piece from the start position to the end position, return if the game should carry on"""
        this_move: ChessMove = self.move_parser.parse_move(start, end, self.board, self.to_move, self.move_list[-1])
        self.move_parser.make_move(self.board, this_move)
        self.move_list.append(this_move)

        if this_move.checkmate:
            self.winner_color = self.to_move
            return False
        if this_move.stalemate:
            self.winner_color = None
            return False


        if (self.to_move == PieceColor.WHITE):
            self.to_move = PieceColor.BLACK
        else:
            self.to_move = PieceColor.WHITE

        return True


    def render_board(self) -> str:
        """ Render the current board state in a code block to preserve whitespace """
        rendered_board = "```" + self.renderer.render(self.board) + "```"
        return rendered_board


    def render_board_image(self, file_name: str) -> str:
        """ Render the current board as an image and save it to the given filename """
        return self.renderer.render_file(self.board, self.move_list[-1], file_name)


    def get_color_to_move(self):
        """ Return the current color to move """
        return self.to_move


    # All shit around this.