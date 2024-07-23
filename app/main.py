import discord
from discord.ext import commands
import yaml
import logging
import os

logger = logging.getLogger('discord')
logger_format = logging.Formatter('%(asctime)s %(levelname)s \t %(message)s', '%Y-%m-%d %H:%M:%S')
file_handler = logging.FileHandler('data/log.txt')
file_handler.setFormatter(logger_format)
logger.addHandler(file_handler)

with open('app/config.yaml', 'r') as file:
    config = yaml.safe_load(file)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=config['CommandPrefix'], intents=intents)

async def load_cogs():
    for filename in os.listdir('app/cogs'):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                logger.info(f'Successfully loaded extension: cogs.{filename[:-3]}')
            except Exception as e:
                logger.error(f'Failed to load extension cogs.{filename[:-3]}: {e}')

async def list_commands():
    for command in bot.tree.walk_commands():
        logger.info(f'Command: {command.name} - Description: {command.description}')

@bot.event
async def on_connect():
    await load_cogs()
    await bot.tree.sync()

@bot.event
async def on_ready():
    logger.info('Logged in as ' + bot.user.name)
    logger.info(f'Guilds: {", ".join(x.name for x in bot.guilds)}')
    await list_commands()

@bot.event
async def on_message(message):
    # We do not want the bot to reply to itself
    if message.author == bot.user:
        return
    # Otherwise process command
    else:
        await bot.process_commands(message)

    
bot.run(config['Token'])



# print(config)