import os
import discord
import logging
import traceback
from discord.ext.commands import Context

from discord.ext import commands
from dotenv import load_dotenv
from src.chess_piece import PieceColor
from src.games_manager import GamesManager
from src.embed_engine import EmbedEngine

logging.basicConfig(
    filename='./logging/logs.txt',
    format='%(asctime)s: '
           '%(filename)s: '
           '%(levelname)s: '
           '%(funcName)s(): '
           '%(lineno)d: '
           '%(message)s')
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

games_manager = GamesManager()

intents = discord.Intents.default()
intents.members = True

embeds = EmbedEngine()

client = commands.Bot(command_prefix='$', intents=intents)


@client.event
async def on_ready():
    """ Function for when the discord bot is ready for interraction """
    LOGGER.info("Bot has connected to Discord")
    print(f'{client.user} has connected to Discord!')


@client.command(name='foo')
async def _foo(ctx: Context, arg):
    """ Test command to check the discord bot is connected """
    LOGGER.info("Foo command sent")
    await ctx.send(arg)


@client.command(name='challenge', pass_context=True)
async def _challenge(ctx: Context, user: discord.User):
    """ Allow a user to challenge another user to a chess game """
    LOGGER.info("Challenge command sent")
    try:
        games_manager.extend_challenge(ctx.author, user)
        challenge_extended_embed = embeds.extend_challenge(user)
        await ctx.send(embed = challenge_extended_embed)
    except Exception as error:
        LOGGER.exception(f"Exception while trying to perform challenge command: {error}")
        error_embed = embeds.error(traceback.format_exc())
        await ctx.send(embed = error_embed)


@client.command(name='challenges')
async def _challenges(ctx: Context):
    """ Get a list of challenged users """
    LOGGER.info("Challenges command sent")
    challenged_users = [ctx.guild.get_member(x).mention for x in games_manager.get_challenges(ctx.author)]
    challenged_users_str = '\n'.join(challenged_users)
    challenges_embed = embeds.challenges(f'\n{challenged_users_str}')
    await ctx.send(embed = challenges_embed)


@client.command(name='accept')
async def _accept(ctx: Context, user: discord.User):
    """ Accept a specific challenge """
    LOGGER.info("Accept command sent")
    try:
        games_manager.accept_challenge(ctx.author, user)
        challenge_accepted_embed = embeds.accept_challenge(user)
        await ctx.send(embed = challenge_accepted_embed)

        created_game = games_manager.find_game_for_user(ctx.author)
        current_move_embed, current_move_file = embeds.current_move(created_game.white, PieceColor.WHITE, games_manager.render_location(created_game))
        await ctx.send(embed=current_move_embed, file=current_move_file)
    except Exception as error:
        LOGGER.exception(f"Exception while trying to perform accept command: {error}")
        error_embed = embeds.error(traceback.format_exc())
        await ctx.send(embed=error_embed)


@client.command(name='move')
async def _move(ctx: Context, move_start, move_end):
    """ Perform a move in the game """
    LOGGER.info("Move command sent")
    sent_message: discord.Message = None
    try:
        current_game = games_manager.find_game_for_user(ctx.author)

        # Parse the move
        if (current_game.game.move(move_start, move_end)):
            # Make the visuals
            current_user, piece_color = games_manager.find_current_user_for_game(current_game)
            current_move_embed, current_move_file = embeds.current_move(current_user, piece_color, games_manager.render_location(current_game))
            sent_message = await ctx.send(embed=current_move_embed, file=current_move_file)
        else:
            # Game is over
            if current_game.game.winner_color == None:
                game_end_embed, game_end_file = embeds.game_draw(current_game.white, current_game.black, games_manager.render_location(current_game))
                await ctx.send(embed=game_end_embed, file=game_end_file)
            else:
                winner_user = current_game.white if current_game.game.winner_color == PieceColor.WHITE else current_game.black
                loser_user = current_game.black if current_game.game.winner_color == PieceColor.WHITE else current_game.white
                game_end_embed, game_end_file = embeds.game_end(winner_user, loser_user, games_manager.render_location(current_game))
                await ctx.send(embed=game_end_embed, file=game_end_file)
            games_manager.remove_current_game_for_user(current_game.white)
    except Exception as error:
        LOGGER.exception(f"Exception while trying to perform move command: {error}")
        error_embed = embeds.error(traceback.format_exc())
        await ctx.send(embed=error_embed)


@client.command(name='stop')
async def _stop(ctx: Context):
    LOGGER.info("Stop command sent")
    """ Stop the bot """
    await ctx.bot.logout()

# Establish commands for creating a challenge, making moves, resigning etc.
# Establish aliases

def main():
    client.run(TOKEN)


if __name__ == "__main__":
    main()