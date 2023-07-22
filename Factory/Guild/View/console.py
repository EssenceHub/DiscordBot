import discord


class ConsoleUI(discord.ui.View):
    def __init__(self):
        super().__init__()

        # Embed
        self.embed = discord.Embed()
        self.embed.color = 0x800080

        # Buttons
        self.guild_button = discord.ui.Button(label="Guild", style=discord.ButtonStyle.blurple, row=1)
        self.party_button = discord.ui.Button(label="Parties", style=discord.ButtonStyle.blurple, row=1)
        self.roles_button = discord.ui.Button(label="Roles", style=discord.ButtonStyle.blurple, row=1)
        self.moderation_button = discord.ui.Button(label="Moderation", style=discord.ButtonStyle.blurple, row=1)
        
        # Modals
        # Selections