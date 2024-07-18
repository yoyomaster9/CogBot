import discord
from discord.ext import commands

import cogs.utilities
import cogs.button
import cogs.tictactoe

async def load_all(bot):
    for cog in commands.Cog.__subclasses__():
        await bot.add_cog(cog(bot))
