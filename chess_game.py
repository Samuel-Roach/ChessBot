import game_constants

from game_renderer import ChessRenderer
from chess_piece import PieceColor


class ChessGameEngine:
    """ Engine playing a game of chess """

    board = game_constants.DEFAULT_BOARD
    renderer = None
    to_move = PieceColor.WHITE


    def __init__(self) -> None:
        # Create the basic board
        self.renderer = ChessRenderer()
        pass


    # Move


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

    # Maybe make a class called ChessMove