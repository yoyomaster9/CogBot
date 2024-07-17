import discord
from discord.ext import commands
import yaml

with open('app/config.yaml', 'r') as file:
    config = yaml.safe_load(file)

class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description = 'Checks to see if the bot is responsive',
                    help = 'Responds with Pong!',
                    brief = 'Responds with Pong!')
    async def ping(self, ctx):
        print('ping?')
        await ctx.send('Pong! {}ms'.format(round(self.bot.latency*1000, 1)))

    @commands.command(brief = 'Logs out of all servers. ADMIN ONLY',
                    description  = 'Logs out of all servers.\nONLY FOR ADMIN USE!')
    async def logout(self, ctx):
        if ctx.author.id == config['AdminID']:
            await ctx.send('Logging out!!')
            await self.bot.close()
        else:
            await ctx.send('You\'re not an admin!')

    @commands.command(description = 'Returns information on the bot.',
                    brief = 'Returns information on the bot.')
    async def about(self, ctx):
        embed=discord.Embed(
            title="CogBot",
            description="Personal ",
            color=discord.Color.orange()  )
        embed.set_author(name=self.bot.user.display_name, url="https://github.com/yoyomaster9/CogBot", icon_url=self.bot.user.avatar)
        embed.add_field(name="*Italics*", value="Surround your text in asterisks ()", inline=False)
        embed.add_field(name="**Bold**", value="Surround your text in double asterisks ()", inline=False)
        embed.add_field(name="__Underline__", value="Surround your text in double underscores (\_\_)", inline=False)
        embed.add_field(name="~~Strikethrough~~", value="Surround your text in double tildes (\~\~)", inline=False)
        embed.add_field(name="`Code Chunks`", value="Surround your text in backticks (\`)", inline=False)
        embed.add_field(name="Blockquotes", value="> Start your text with a greater than symbol (\>)", inline=False)
        embed.add_field(name="Secrets", value="||Surround your text with double pipes (\|\|)||", inline=False)
        await ctx.send(embed=embed)