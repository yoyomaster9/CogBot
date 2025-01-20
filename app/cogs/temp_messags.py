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
    
    @discord.app_commands.command(
        name = 'setdelay',
        description = 'Sets the time delay for temp message' 
    )
    async def setdelay(self, interaction: discord.Interaction, delay: str) -> None:

        pattern = r'(?:(\d+)\s*(?:hours|hour|hrs|hr|h))?\s*(?:(\d+)\s*(?:minutes|minute|mins|min|m))?\s*(?:(\d+)\s*(?:seconds|second|secs|sec|s))?'
        matches = re.findall(pattern, delay)
        l = [''.join(m[i] for m in matches) for i in range(3)]
        l = [int(x) if x != '' else 0 for x in l]

        sec = l[0] * 3600 + l[1] * 60 + l[2]
        config['TempMessageTime'] = sec

        
        hours, minutes = divmod(sec, 3600)
        minutes, seconds = divmod(minutes, 60)
        output = ''
        if hours > 0:
            output += f'{hours}hr '
        if minutes > 0:
            output += f'{minutes}m '
        if seconds > 0:
            output += f'{seconds}s'

        
        await interaction.response.send_message(f'Temp message chat delay set to {output}')
        temp_channel = self.bot.get_channel(config['TempMessageChannelID'])
        await temp_channel.edit(topic = f"Messages will be deleted after {output} ")  

async def setup(bot):

    await bot.add_cog(TempMessageCog(bot))