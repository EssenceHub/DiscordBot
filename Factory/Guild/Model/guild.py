import discord
import sqlite3

class Guild():
    def __init__(self, interaction: discord.Interaction):
        self.interaction = interaction
        self.guild = interaction.guild
        self.bot_count = len([member for member in interaction.guild.members if member.bot])

        self.db = sqlite3.connect("essence.db")
        self.cursor = self.db.cursor()