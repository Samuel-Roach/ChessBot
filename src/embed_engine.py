from dis import disco
import discord
import constants.message_constants as message_constants

from src.chess_piece import PieceColor
from src.games_manager import GamesManager

class EmbedEngine:
    """ Engine for generating relevant discord Embeds """


    def __init__(self) -> None:
        pass


    def embed(self, title, description, color):
        """ Returns an embed with the given values """
        return discord.Embed(
            title=title,
            description=description,
            color=color
        )


    def error(self, error_message,
              title=message_constants.ERROR_TITLE,
              description=message_constants.ERROR_DESCRIPTION,
              color=message_constants.ERROR_COLOR) -> discord.Embed:
        """ Returns an embed for error messages """
        return self.embed(title, description.format(error_message), color)


    def info(self, title=message_constants.INFO_TITLE,
             description=message_constants.INFO_DESCRIPTION,
             color=message_constants.INFO_COLOR) -> discord.Embed:
        """ Returns an embed for information """
        return self.embed(title, description, color)


    def confirm(self, title=message_constants.CONFIRM_TITLE,
                description=message_constants.CONFIRM_DESCRIPTION,
                color=message_constants.CONFIRM_COLOR) -> discord.Embed:
        """ Returns an embed for confirmation """
        return self.embed(title, description, color)


    def challenges(self, users: str,
                         title=message_constants.CHALLENGES_TITLE,
                         description=message_constants.CHALLENGES_DESCRIPTION,
                         color=message_constants.CHALLENGES_COLOR):
        """ Returns the embed for a challenge being extended """
        return self.embed(title, description.format(users), color)


    def extend_challenge(self, user: discord.User,
                         title=message_constants.EXTENDED_TITLE,
                         description=message_constants.EXTENDED_DESCRIPTION,
                         color=message_constants.EXTENDED_COLOR):
        """ Returns the embed for a challenge being extended """
        return self.embed(title, description.format(user.mention), color)


    def accept_challenge(self, user: discord.User,
                         title=message_constants.ACCEPTED_TITLE,
                         description=message_constants.ACCEPTED_DESCRIPTION,
                         color=message_constants.ACCEPTED_COLOR):
        """ Returns the embed for a challenge being accepted """
        return self.embed(title, description.format(user.mention), color)


    def current_move(self, user: discord.User,
                    user_color: PieceColor,
                    current_board_location: str,
                    title=message_constants.CURRENT_MOVE_TITLE,
                    description=message_constants.CURRENT_MOVE_DESCRIPTION,
                    color=message_constants.CURRENT_MOVE_COLOR):
        """ Returns the embed for the current move to be made """
        file = discord.File(current_board_location, filename="board.png")
        board_embed = self.embed(title, description.format(user.mention, user_color.name), color)
        board_embed.set_image(url="attachment://board.png")
        return board_embed, file

    def game_end(self, winner_user: discord.User,
                loser_user: discord.User,
                current_board_location: str,
                title=message_constants.GAME_END_TITLE,
                description=message_constants.GAME_END_DESCRIPTION,
                color=message_constants.GAME_END_COLOR):
        """ Returns the embed for the winner """
        file = discord.File(current_board_location, filename="board.png")
        winner_embed = self.embed(title.format(winner_user.display_name), description.format(winner_user.display_name, loser_user.display_name), color)
        winner_embed.set_image(url="attachment://board.png")
        return winner_embed, file
    
    def game_draw(self, first_user: discord.User,
                  second_user: discord.User,
                  current_board_location: str,
                  title=message_constants.GAME_DRAW_TITLE,
                  description=message_constants.GAME_DRAW_DESCRIPTION,
                  color=message_constants.GAME_DRAW_COLOR):
        """ Returns the embed for a draw """
        file = discord.File(current_board_location, filename="board.png")
        draw_embed = self.embed(title, description.format(first_user.display_name, second_user.display_name), color)
        draw_embed.set_image(url="attachment://board.png")
        return draw_embed, file