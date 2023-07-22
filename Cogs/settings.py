# This file will be for Settings configuration
import discord
import sqlite3
from discord import app_commands
from discord.ext import commands
from datetime import datetime, timedelta

from Factory.Settings.Model.data import Data as SettingsData
from Factory.Settings.View.console import ConsoleUI as SettingsConsoleUI
from Factory.Settings.Controller.callbacks import Callbacks as SettingsCallbacks

# --------------------------------------------------------------------------------------------------------------------------------------------------------------

# Command cog class
class Settings(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(description="User and Server settings")
    async def settings(self, interaction: discord.Interaction):
        settings_logic = SettingsCallbacks(SettingsData(interaction))

        await interaction.response.send_message(embed=settings_logic.embed, view=settings_logic.console, ephemeral=True)

# Setup function
async def setup(bot: commands.Bot):
    print("Settings Loaded")
    await bot.add_cog(Settings(bot))