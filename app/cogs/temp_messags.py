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

def format_seconds(sec: int) -> str:
    hours, minutes = divmod(sec, 3600)
    minutes, seconds = divmod(minutes, 60)
    output = []
    if hours > 0:
        output.append(f'{hours}hr')
    if minutes > 0:
        output.append(f'{minutes}m')
    if seconds > 0:
        output.append(f'{seconds}s')
    return ' '.join(output)


class TempMessageCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.temp_channels = config['TempMessageChannels']
        self.delay_map = {x['ChannelID']: x['Time'] for x in self.temp_channels.values()}

    @commands.Cog.listener()
    async def on_ready(self):

        for channel_name, kwargs in self.temp_channels.items():
            channel = self.bot.get_channel(kwargs['ChannelID'])
            await channel.purge()
            await channel.send(f'Welcome to the {channel_name}. Messages will be deleted after {format_seconds(kwargs["Time"])}')

        for channel_name, kwargs in self.temp_channels.items():
            channel = self.bot.get_channel(kwargs['ChannelID'])
            channel_name = f'{channel_name}-{format_seconds(kwargs["Time"])}'.lower().replace(' ', '-')
            await channel.edit(name = channel_name, topic = f"Messages will be deleted after {format_seconds(kwargs['Time'])} seconds")
             
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id in self.delay_map:
            await asyncio.sleep(self.delay_map[message.channel.id])
            await message.delete()


async def setup(bot):
    await bot.add_cog(TempMessageCog(bot))