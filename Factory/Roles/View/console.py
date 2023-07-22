import discord

class ConsoleUI(discord.ui.View):
    def __init__(self):
        super().__init__()

        # Embed
        self.embed = discord.Embed()
        self.embed.color = 0x800080
        
        # Selections
        self.role_selection = discord.ui.Select(placeholder="Choose a role")