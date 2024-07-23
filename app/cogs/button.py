import discord
from discord.ext import commands
import yaml

with open('app/config.yaml', 'r') as file:
    config = yaml.safe_load(file)

class ButtonCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @discord.app_commands.command(
                description = 'Makes a button that you can click',
                # help = 'Makes a button.',
                # brief = 'Makes a button.'
                )
    async def button(self, ctx):
        await ctx.send('Pong! {}ms'.format(round(self.bot.latency*1000, 1)))

        # view = discord.ui.View() # Establish an instance of the discord.ui.View class
        # style = discord.ButtonStyle.red  # The button will be gray in color
        # item = discord.ui.Button(style=style, label="Click me!", url="https://discordpy.readthedocs.io/en/master")  # Create an item to pass into the view class.
        # view.add_item(item=item)  # Add that item into the view class
        # await ctx.send("This message has buttons!", view=view)  # Send your message with a button.
        await ctx.send('part 2!', view = Button())

class Button(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="test your luck",style=discord.ButtonStyle.blurple)
    async def unclicked_button(self,interaction:discord.Interaction, button: discord.Button):
        button.style = discord.ButtonStyle.green
        button.label = 'you win!'
        await interaction.response.edit_message(view=self)


    @discord.ui.button(label="test your luck",style=discord.ButtonStyle.blurple)
    async def unclicked_button2(self,interaction:discord.Interaction, button: discord.Button):
        button.style = discord.ButtonStyle.red
        button.label = 'you lose!'
        await interaction.response.edit_message(view=self)


async def setup(bot):
    await bot.add_cog(ButtonCog(bot))
