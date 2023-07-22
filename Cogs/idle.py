import discord
from discord import app_commands
from discord.ext import commands

from Factory.Idle.View.console import ConsoleUI
from Factory.Idle.Model.player import Player
from Factory.Idle.Controller.callbacks import Callbacks


class Idle(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Shows the player's idle game console
    @app_commands.command(description='Idle Game!')
    async def idle(self, interaction: discord.Interaction):
        tester = interaction.guild.get_role(1062407758718185612)
        my_id = 491289245974003722

        if tester in interaction.user.roles or interaction.user.id == my_id:
            # Gets idle game logic
            idle_logic = Callbacks(ConsoleUI(), Player(interaction))

            await interaction.response.send_message(embed=idle_logic.embed, view=idle_logic.console)
        else:
            await interaction.response.send_message(f"Essence Idle is a WIP, please message <@{my_id}> if you're interested in testing. Please be warned that data will be consistently wiped and corrupted.", ephemeral=True)

    
async def setup(bot: commands.Bot):
    print("Idle Loaded")
    await bot.add_cog(Idle(bot))