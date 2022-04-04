import os
import discord
import traceback

from discord.ext import commands
from dotenv import load_dotenv
from src.chess_piece import PieceColor
from src.games_manager import GamesManager
from src.embed_engine import EmbedEngine

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
    print(f'{client.user} has connected to Discord!')


@client.command(name='foo')
async def _foo(ctx, arg):
    """ Test command to check the discord bot is connected """
    await ctx.send(arg)


@client.command(name='challenge', pass_context=True)
async def _challenge(ctx, user: discord.User):
    """ Allow a user to challenge another user to a chess game """
    try:
        games_manager.extend_challenge(ctx.author, user)
        challenge_extended_embed = embeds.extend_challenge(user)
        await ctx.send(embed = challenge_extended_embed)
    except Exception as error:
        error_embed = embeds.error(traceback.format_exc())
        await ctx.send(embed = error_embed)


@client.command(name='challenges')
async def _challenges(ctx):
    """ Get a list of challenged users """
    challenged_users = [ctx.guild.get_member(x).mention for x in games_manager.get_challenges(ctx.author)]
    challenged_users_str = '\n'.join(challenged_users)
    challenges_embed = embeds.challenges(f'\n{challenged_users_str}')
    await ctx.send(embed = challenges_embed)


@client.command(name='accept')
async def _accept(ctx, user: discord.User):
    """ Accept a specific challenge """
    try:
        games_manager.accept_challenge(ctx.author, user)
        challenge_accepted_embed = embeds.accept_challenge(user)
        await ctx.send(embed = challenge_accepted_embed)

        created_game = games_manager.find_game_for_user(ctx.author)
        current_move_embed, current_move_file = embeds.current_move(created_game.white, PieceColor.WHITE, games_manager.render_location(created_game))
        await ctx.send(embed=current_move_embed, file=current_move_file)
            
    except Exception as error:
        error_embed = embeds.error(traceback.format_exc())
        await ctx.send(embed=error_embed)


@client.command(name='move')
async def _move(ctx, move_start, move_end):
    """ Perform a move in the game """
    try:
        current_game = games_manager.find_game_for_user(ctx.author)

        # Parse the move
        current_game.game.move(move_start, move_end)

        # Make the move
        current_user, piece_color = games_manager.find_current_user_for_game(current_game)
        current_move_embed, current_move_file = embeds.current_move(current_user, piece_color, games_manager.render_location(current_game))
        await ctx.send(embed=current_move_embed, file=current_move_file)
    except Exception as error:
        error_embed = embeds.error(traceback.format_exc())
        await ctx.send(embed=error_embed)


@client.command(name='stop')
async def _stop(ctx):
    """ Stop the bot """
    await ctx.bot.logout()

# Establish commands for creating a challenge, making moves, resigning etc.
# Establish aliases

client.run(TOKEN)