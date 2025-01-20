from typing import Coroutine, List
from discord.ext import commands
import discord
import random

class DiscordRouletteCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(
        name = 'roulette',
        description = 'Start Ban Roulette')
    async def roulette(self, interaction, winner_buttons: int, loser_buttons: int):
        await interaction.response.send_message('testing!', view=DiscordRouletteView(winner_buttons=winner_buttons, loser_buttons=loser_buttons))

class DiscordRouletteView(discord.ui.View):
    # View to hold buttons 

    def __init__(self, fail_type = None, winner_buttons = 6, loser_buttons = 1):
        super().__init__(timeout=300)
        # Create n buttons where one has consequnces with type
        self.fail_type = fail_type
        buttons = [DiscordRouletteButton(fail_type=self.fail_type) for i in range(winner_buttons)] + [DiscordRouletteButton(fail_type=self.fail_type, loser=True) for i in range(loser_buttons)] 
        random.shuffle(buttons)
        for b in buttons:
            self.add_item(b)
        
    async def on_timeout(self):
        await super().on_timeout()
        print('timeout!')
        for child in self.children:
            child.disabled = True
        # await self.message.edit(view=self)
        self.stop()

class DiscordRouletteButton(discord.ui.Button):

    def __init__(self, fail_type = None, loser = False):
        super().__init__(label = '?')
        self.loser = loser # will determine if button triggers win/loss 
        # self.view = DiscordRouletteView
        self.style = discord.ButtonStyle.grey
    

    # "on-click" event
    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None


        if self.loser == False:
            self.style = discord.ButtonStyle.green
            self.label = interaction.user
        else:
            self.style = discord.ButtonStyle.red
            self.label = 'loser!'
            for child in self.view.children:
                child.disabled = True
            self.view.stop()

        await interaction.response.edit_message(view=self.view)




async def setup(bot):
    await bot.add_cog(DiscordRouletteCog(bot))
