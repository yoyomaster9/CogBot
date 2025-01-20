from discord.ext import commands
import discord
import yaml
import logging
import json
import os

with open('app/config.yaml', 'r') as file:
    config = yaml.safe_load(file)



logger = logging.getLogger('discord')

class BestOfCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.dir = 'data/cogs/best_of.json'
        if os.path.exists(self.dir):
            self.load()
        else:
            self.data = []
            self.save()

    def save(self):
        with open(self.dir, 'w') as file:
            json.dump(self.data, file)

    def load(self):
        with open(self.dir, 'r') as file:
            self.data = json.load(file)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User):
        if reaction.count == 4 and reaction.emoji == '⭐' and reaction.message.id not in self.data:
            self.data.append(reaction.message.id)
            self.save()
            channel = self.bot.get_channel(config['BestOfChannelID'])
            await channel.send(f'{reaction.message.author.mention}: {reaction.message.content}\n{reaction.message.jump_url}')


async def setup(bot):
    await bot.add_cog(BestOfCog(bot))