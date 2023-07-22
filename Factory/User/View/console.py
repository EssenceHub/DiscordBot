import discord


class ConsoleUI(discord.ui.View):
    def __init__(self):
        super().__init__()

        # Embed
        self.embed = discord.Embed()

        # Buttons
        self.profile_button = discord.ui.Button(label="Profile", style=discord.ButtonStyle.blurple, row=1)
        self.permissions_button = discord.ui.Button(label="Permissions", style=discord.ButtonStyle.blurple, row=1)
        self.party_button = discord.ui.Button(label="Party", style=discord.ButtonStyle.blurple, row=1)
        
        # Modals
        # Selections