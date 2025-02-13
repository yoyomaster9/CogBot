from discord.ext import commands
import discord
import yaml
import logging
import asyncio
from pytz import timezone
import re

with open('app/config.yaml', 'r') as file:
    config = yaml.safe_load(file)

logger = logging.getLogger('discord')

class TempMessageCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        temp_channel = self.bot.get_channel(config['TempMessageChannelID'])
        await temp_channel.edit(topic = f"Messages will be deleted after {config['TempMessageTime']} seconds")   
             
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == config['TempMessageChannelID']:
            s = f"[{ message.created_at.astimezone(timezone('US/Pacific')).strftime('%m/%d/%Y %H:%M:%S') }] {message.author.display_name}: {message.content}\n"
            # with open('data/cogs/temp_messages.txt', 'a') as file:
            #     file.write(s)
            await asyncio.sleep(config['TempMessageTime'])
            await message.delete()


async def setup(bot):

    await bot.add_cog(TempMessageCog(bot))