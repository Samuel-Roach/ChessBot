import constants.game_constants as game_constants
import os

from PIL import Image
from src.chess_piece import ChessPiece, PieceColor, PieceType
from src.move_parser import ChessMove

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


    def _find_king(self, board: list, color: PieceColor):
        """ Find the color king within the board and return its location """
        for x in range(0, 8):
            for y in range(0, 8):
                current_piece: ChessPiece = board[y][x]
                if current_piece != None and current_piece.color == color and current_piece.piece_type == PieceType.KING:
                    return (x, y)

        raise Exception("No king found")


    def render(self, board: list):
        """ Return a string representation of the board """
        render_rows = []

        row_no = 1
        for row in board:
            render_rows.append(self._render_row(row, row_no))
            row_no += 1

        return '\n'.join(render_rows)


    def render_file(self, board: list, previous_move: ChessMove, save_name: str):
        """ Return the string location of a representation image of this board """
        background = Image.open(self.ICONS["BOARD"], 'r').convert('RGBA').rotate(180)
        final_image = Image.new('RGBA', (1200, 1200))
        final_image.paste(background)

        # Previous move highlighting
        if (previous_move != None):
            highlight_image = Image.open(self.ICONS["PREVIOUS_MOVE"], 'r').convert('RGBA')
            start_move_offset = (1050 - (150 * previous_move.start_move[0]), (150 * previous_move.start_move[1]))
            end_move_offset = (1050 - (150 * previous_move.end_move[0]), (150 * previous_move.end_move[1]))
            final_image.paste(highlight_image, start_move_offset, highlight_image)
            final_image.paste(highlight_image, end_move_offset, highlight_image)

        if (previous_move != None and previous_move.check):
            check_image = Image.open(self.ICONS["CHECK_MOVE"], 'r').convert('RGBA')
            check_color = PieceColor.WHITE if previous_move.piece.color == PieceColor.BLACK else PieceColor.BLACK
            checked_king = self._find_king(board, check_color)
            check_offset = (1050 - (150 * checked_king[0]), (150 * checked_king[1]))
            final_image.paste(check_image, check_offset, check_image)

        # Piece rendering
        for x in range(0, 8):
            for y in range(0, 8):
                piece: ChessPiece = board[y][x]
                if piece != None:
                    piece_image = Image.open(self.ICONS[piece.color][piece.piece_type]["image"], 'r').convert('RGBA').rotate(180)
                    offset = (1050 - (150 * x), (150 * y))
                    final_image.paste(piece_image, offset, piece_image)

        if not os.path.exists('board_renders/'):
            os.mkdir('board_renders')

        if os.path.exists(f'board_renders/{save_name}.png'):
            os.remove(f'board_renders/{save_name}.png')

        final_image.rotate(180).save(f'board_renders/{save_name}.png')
        return f'board_renders/{save_name}.png'
