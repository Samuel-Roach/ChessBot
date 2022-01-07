import game_constants
import os

from chess_piece import ChessPiece
from PIL import Image

class ChessRenderer:
    """ Renderer for a game of chess """

    # Storing all the icons that we may use throughout a game
    ICONS = game_constants.GAME_ICONS

    def __init__(self) -> None:
        pass


    def _render_row(self, row: list, row_no: int):
        """ Return a string representation of a row on a chess board """
        column = 1
        tile_color = self.ICONS["BLACK_TILE"] if row_no % 2 == column % 2 else self.ICONS["WHITE_TILE"]
        render_array = []

        for item in row:
            if type(item) is ChessPiece:
                render_array.append(self.ICONS[item.color][item.piece_type])
            else:
                render_array.append(tile_color)

            # Flip tile color
            column += 1
            tile_color = self.ICONS["BLACK_TILE"] if row_no % 2 == column % 2 else self.ICONS["WHITE_TILE"]

        return ' '.join(render_array)


    def render(self, board: list):
        """ Return a string representation of the board """
        render_rows = []

        row_no = 1
        for row in board:
            render_rows.append(self._render_row(row, row_no))
            row_no += 1

        return '\n'.join(render_rows)


    def render_file(self, board: list, save_name: str):
        """ Return the string location of a representation image of this board """
        background = Image.open(self.ICONS["BOARD"], 'r').convert('RGBA').rotate(180)
        final_image = Image.new('RGBA', (1200, 1200))
        final_image.paste(background)

        position = (0, 0)
        for row in board:
            for item in row:
                if type(item) is ChessPiece:
                    item_image = Image.open(self.ICONS[item.color][item.piece_type]["image"], 'r').convert('RGBA').rotate(180)
                    offset = ((150 * position[0]), (150 * position[1]))
                    final_image.paste(item_image, offset, item_image)
                position = (list(position)[0] + 1, list(position)[1]) 
            position = (0, list(position)[1] + 1) 

        if os.path.exists(f'board_renders/{save_name}.png'):
            os.remove(f'board_renders/{save_name}.png')

        final_image.rotate(180).save(f'board_renders/{save_name}.png')
        return f'board_renders/{save_name}.png'
