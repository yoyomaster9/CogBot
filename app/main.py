import discord
from discord.ext import commands
# from cogs import utilities
import cogs
import yaml
import logging


logger = logging.getLogger('discord')
logger_format = logging.Formatter('%(asctime)s %(levelname)s \t %(message)s', '%Y-%m-%d %H:%M:%S')
file_handler = logging.FileHandler('data/log.txt')
file_handler.setFormatter(logger_format)
logger.addHandler(file_handler)

with open('app/config.yaml', 'r') as file:
    config = yaml.safe_load(file)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=config['CommandPrefix'], intents=intents)

@bot.event
async def on_message(message):
    # We do not want the bot to reply to itself
    if message.author == bot.user:
        return
    # Otherwise process command
    else:
        await bot.process_commands(message)

@bot.event
async def on_ready():
    logger.info('Logged in as ' + bot.user.name)
    logger.info(f'Guilds: {", ".join(x.name for x in bot.guilds)}')

    await cogs.load_all(bot)

    


    # print('---------------------')
    # for g in bot.guilds:
    #     print('Logged into {}'.format(g))
bot.run(config['Token'])



# print(config)