import discord
import sqlite3

from datetime import datetime

class Data:
    def __init__(self, interaction: discord.Interaction):
        self.timestamp = round(datetime.now().timestamp())
        self.interaction = interaction
        self.host = interaction.user

        self.db = sqlite3.connect("vulcan.db")
        self.cursor = self.db.cursor()

        self.bet_name = None
        self.winner = None
        self.options = []

        self.player_choice = 0
        self.player_bet_amount = None

    def already_bet(self, interaction: discord.Interaction, bet_name: str):
        self.cursor.execute("SELECT bets_made FROM bets WHERE name = ?", (bet_name,))
        bets_made = self.cursor.fetchone(); bets_made = bets_made[0] or ""

        if str(interaction.user.id) in bets_made:
            return True
        else:
            return False
        
    def not_registered(self, user: discord.Member):
        self.cursor.execute("SELECT roblox_user FROM players WHERE id = ?", (user.id,))
        roblox_user = self.cursor.fetchone()

        if roblox_user == None:
            return True
        else:
            return False