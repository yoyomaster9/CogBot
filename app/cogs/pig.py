from typing import Coroutine
import discord
from discord.ext import commands
import yaml
import logging
import random

with open('app/config.yaml', 'r') as file:
    config = yaml.safe_load(file)

logger = logging.getLogger('discord')

class PigCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @discord.app_commands.command(
        name = 'pig',
        description = 'Start a game of Pig with another player'
        )
    async def pig(self, interaction: discord.Interaction, player2: discord.User, excluded_numbers: str):
        await interaction.response.send_message(f'Game start!', view = PigView(interaction.user, player2, excluded_numbers))

class PigView(discord.ui.View):
    def __init__(self, player1: discord.User, player2: discord.User, excluded_numbers: str):
        super().__init__()
        self.player1 = player1
        self.player2 = player2
        self.active_player = random.choice((player1, player2))
        self.excluded_numbers = [int(x) for x in excluded_numbers if x in '123456']
        self.rolls = []
        self.add_item(PigRollButton())
        self.add_item(PigStopButton())
    
    async def update(self):
        # msg = 
        pass

    def roll(self):
        n = random.randint(1, 6)
        # if n in ex
        

    def stop(self):


        
        # self.active_player = 

        if self.active_player == self.player1:
            self.active_player = self.player2
        else:
            self.active_player = self.player1

class PigRollButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label='Roll', style=discord.ButtonStyle.green)

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user != self.view.active_player:
            return False
        await super().interaction_check(interaction)

    async def callback(self, interaction: discord.Interaction):
        await super().callback(interaction)

class PigStopButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label='Stop', style=discord.ButtonStyle.red)

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user != self.view.active_player:
            return False
        await super().interaction_check(interaction)


async def setup(bot):
    await bot.add_cog(PigCog(bot))