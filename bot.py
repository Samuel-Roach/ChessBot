import os
import discord

from discord.ext import commands
from dotenv import load_dotenv
from chess_piece import PieceColor
from games_manager import GamesManager
from embed_engine import EmbedEngine

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

games_manager = GamesManager()

intents = discord.Intents.default()
intents.members = True

embeds = EmbedEngine()

client = commands.Bot(command_prefix='$', intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.command(name='foo')
async def _foo(ctx, arg):
    await ctx.send(arg)

@client.command(name='challenge', pass_context=True)
async def _challenge(ctx, user: discord.User):
    try:
        games_manager.extend_challenge(ctx.author, user)
        challenge_extended_embed = embeds.extend_challenge(user)
        await ctx.send(embed = challenge_extended_embed)
    except Exception as error:
        error_embed = embeds.error(error)
        await ctx.send(embed = error_embed)


@client.command(name='challenges')
async def _challenges(ctx):
    challenged_users = [ctx.guild.get_member(x).mention for x in games_manager.get_challenges(ctx.author)]
    challenged_users_str = '\n'.join(challenged_users)
    challenges_embed = embeds.challenges(f'\n{challenged_users_str}')
    await ctx.send(embed = challenges_embed)


@client.command(name='accept')
async def _accept(ctx, user: discord.User):
    try:
        games_manager.accept_challenge(ctx.author, user)
        challenge_accepted_embed = embeds.accept_challenge(user)
        await ctx.send(embed = challenge_accepted_embed)

        created_game = games_manager.find_game_for_user(ctx.author)
        current_move_embed, current_move_file = embeds.current_move(created_game.white, PieceColor.WHITE, games_manager.render_location(created_game))
        await ctx.send(embed=current_move_embed, file=current_move_file)
    except Exception as error:
        error_embed = embeds.error(error)
        await ctx.send(embed=error_embed)


@client.command(name='move')
async def _move(ctx, move_start, move_end):
    try:
        current_game = games_manager.find_game_for_user(ctx.author)

        # Parse the move
        # Make the move
        current_user, piece_color = games_manager.find_current_user_for_game(current_game)
        current_move_embed, current_move_file = embeds.current_move(current_user, piece_color, games_manager.render_location(current_game))
        await ctx.send(embed=current_move_embed, file=current_move_file)
    except Exception as error:
        error_embed = embeds.error(error)
        await ctx.send(embed=error_embed)

# Establish commands for creating a challenge, making moves, resigning etc.

client.run(TOKEN)