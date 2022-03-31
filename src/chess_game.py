import constants.game_constants as game_constants

from src.game_renderer import ChessRenderer
from src.move_parser import MoveParser
from src.chess_piece import PieceColor


class ChessGameEngine:
    """ Engine playing a game of chess """

    board = game_constants.DEFAULT_BOARD
    renderer = None
    move_parser = None
    to_move = PieceColor.WHITE
    move_list = []


    def __init__(self) -> None:
        # Create the basic board
        self.renderer = ChessRenderer()
        self.move_parser = MoveParser()
        self.move_list = [None]
        pass


    # Move
    def move(self, start: str, end: str) -> bool:
        """ Move a piece from the start position to the end position """
        this_move = self.move_parser.parse_move(start, end, self.board, self.to_move, self.move_list[-1])
        self.move_parser.make_move(self.board, this_move)
        self.move_list.append(this_move)

        if (self.to_move == PieceColor.WHITE):
            self.to_move = PieceColor.BLACK
        else:
            self.to_move = PieceColor.WHITE


    def render_board(self) -> str:
        """ Render the current board state in a code block to preserve whitespace """
        rendered_board = "```" + self.renderer.render(self.board) + "```"
        return rendered_board


    def render_board_image(self, file_name: str) -> str:
        """ Render the current board as an image and save it to the given filename """
        return self.renderer.render_file(self.board, file_name)


    def get_color_to_move(self):
        """ Return the current color to move """
        return self.to_move


    # All shit around this.