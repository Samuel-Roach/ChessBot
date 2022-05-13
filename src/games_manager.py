import discord

from dataclasses import dataclass
from discord.errors import InvalidData
from src.chess_game import ChessGameEngine
from src.chess_piece import PieceColor


class GamesManager:
    """ Manage all chess games within the bot."""

    CHALLENGES = {
        # Challenges is a map of UserID to UserID
        # The key is the extender, the value is an array of receivers.
        # e.g. "12345": [12344, 12346, 12347]
    }

    CURRENT_GAMES = {
        # A game maps a game id (the users id's concatenated) to a ChessGame struct
    }

    MAX_CHALLENGES = 5


    @dataclass
    class ChessGame:
        """ A representation of a chess game, with the users and the game itself """
        def __init__(self, white: discord.User, black: discord.User, game: ChessGameEngine) -> None:
            self.white = white
            self.black = black
            self.game = game
            pass


    def __init__(self) -> None:
        pass


    def _check_valid_challenge(self, extender: discord.User, receiver: discord.User):
        """ Checks that the challenge extended is valid """
        extender_challenges = []

        # Check the users challenges are less than the max amount of challenges allowed
        if extender.id in self.CHALLENGES:
            extender_challenges = self.CHALLENGES[extender.id]
            if len(extender_challenges) >= self.MAX_CHALLENGES:
                return False, "You cannot create another challenge without removing another!"
        else:
            return True, ""

        # Check that the challenge doesn't exist
        if receiver.id in extender_challenges:
            return False, f"You have already challenged {receiver.mention}!"
        else:
            # Check that there isn't a current game between these two players
            possible_game_ids = [str(extender.id) + '_' + str(receiver.id), str(receiver.id) + '_' + str(extender.id)]
            if any(possible_game_ids) in self.CURRENT_GAMES:
                return False, f"There is already a game between you and {receiver.mention}!"

        return True, ""


    def extend_challenge(self, extender: discord.User, receiver: discord.User):
        """ Create a challenge from the extender to the receiver """
        valid, error = self._check_valid_challenge(extender, receiver)

        # Create the challenge
        if valid:
            if extender.id in self.CHALLENGES:
                self.CHALLENGES[extender.id].append(receiver.id)
            else:
                self.CHALLENGES[extender.id] = [receiver.id]
        else:
            raise InvalidData(error)


    def get_challenges(self, user: discord.User):
        """ Get the extended challenges from a given user """
        if user.id in self.CHALLENGES:
            return self.CHALLENGES[user.id]
        else:
            return []


    def get_received_challenges(self, user: discord.User):
        """ Get challengers extended to a receiving user """
        challengers = []

        for userid in self.CHALLENGES:
            if user.id in self.CHALLENGES[userid]:
                challengers.append(userid)

        return challengers


    def _check_challenge_exists(self, extender: discord.User, receiver: discord.User):
        """ Checks whether a challenge exists between an extender and receiver """
        if extender.id in self.CHALLENGES:
            extender_challenges = self.CHALLENGES[extender.id]
            if receiver.id in extender_challenges:
                return True, ""

        return False, f"A challenge from {extender.mention} doesn't exist!"


    def _check_valid_acceptance(self, extender: discord.User, receiver: discord.User):
        """ Check that the call to accept a challenge is valid """
        valid, error = self._check_challenge_exists(extender, receiver)

        if valid:
            for game in self.CURRENT_GAMES:
                if str(extender.id) in game or str(receiver.id) in game:
                    return False, "You can only accept a challenge when both players are out of a game."
        else:
            return False, error

        return True, ""


    def accept_challenge(self, acceptor: discord.User, extender: discord.User):
        """ Accept a challenge from the extender as the given acceptor """
        valid, error = self._check_valid_acceptance(extender, acceptor)
        
        if valid:
            game_id = str(extender.id) + '_' + str(acceptor.id)
            game = self.ChessGame(acceptor, extender, ChessGameEngine())
            self.CURRENT_GAMES[game_id] = game

            self.CHALLENGES[extender.id] = self.CHALLENGES[extender.id].remove(acceptor.id)
        else:
            raise InvalidData(error)


    def find_gameid_for_user(self, user: discord.User):
        """ Find the current game id for a user. If no game is found, an error is thrown """
        for game_id in self.CURRENT_GAMES:
            if str(user.id) in game_id:
                return game_id

        raise InvalidData(f"No current game id can be found for {user.mention}")


    def find_game_for_user(self, user: discord.User) -> ChessGame:
        """ Find the current game for a user. If no game is found, an error is thrown """
        return self.CURRENT_GAMES[self.find_gameid_for_user(user)]


    def remove_current_game_for_user(self, user: discord.User):
        game_id = self.find_gameid_for_user(user)
        del self.CURRENT_GAMES[game_id]


    def render_game(self, current_game: ChessGame):
        """ Return the render of a game from it's game_id """
        try:
            return current_game.game.render_board()
        except Exception as e:
            raise InvalidData(f"Failed to render game with error: {e}")


    def render_location(self, current_game: ChessGame):
        """ Render the board for the given game and return the renders location """
        generated_save_name = self.find_gameid_for_user(current_game.white)
        return current_game.game.render_board_image(generated_save_name)


    def find_current_user_for_game(self, current_game: ChessGame):
        """ Find the current player to play given a ChessGame """
        color_to_move = current_game.game.get_color_to_move()
        player_to_move = current_game.white if color_to_move == PieceColor.WHITE else current_game.black
        return player_to_move, color_to_move