import discord

ERROR_TITLE = 'Error'
ERROR_DESCRIPTION = 'An error has occured: {}' # Error message
ERROR_COLOR = discord.Color.red()

INFO_TITLE = 'Information'
INFO_DESCRIPTION = 'Information box'
INFO_COLOR = discord.Color.blue()

CONFIRM_TITLE = 'Confirmation'
CONFIRM_DESCRIPTION = 'Confirmation box'
CONFIRM_COLOR = discord.Color.green()

EXTENDED_TITLE = 'Challenge extended'
EXTENDED_DESCRIPTION = 'A challenge has been extended to {}.' # User
EXTENDED_COLOR = discord.Color.green()

ACCEPTED_TITLE = 'Challenge accepted'
ACCEPTED_DESCRIPTION = 'You have accepted a challenge from {}.' # User
ACCEPTED_COLOR = discord.Color.green()

CHALLENGES_TITLE = 'Current Challenges'
CHALLENGES_DESCRIPTION = 'Here are your current challenges: {}' # List of users
CHALLENGES_COLOR = discord.Color.blue()

CURRENT_MOVE_TITLE = ''
CURRENT_MOVE_DESCRIPTION = '{} to move ({})' # User, Piece.Color
CURRENT_MOVE_COLOR = discord.Color.blue()

GAME_END_TITLE = '{} wins!' # User
GAME_END_DESCRIPTION = '{} wins against {}. \n Final board:' # User, Win type, current board, notation
GAME_END_COLOR = discord.Color.purple()