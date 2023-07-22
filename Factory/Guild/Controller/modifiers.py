from Factory.Guild.View.console import ConsoleUI
from Factory.Guild.Model.guild import Guild

class ConsoleLogic:
    def __init__(self, console: ConsoleUI, guild: Guild):
        # UI
        self.console = console
        self.embed = console.embed
        # Data
        self.guild = guild

        self.Guild_Info_Button()

    # Console Logic
    def Guild_Info_Button(self):
        guild = self.guild.guild
        
        self.embed.title = f"{guild.name}'s Information"
        self.embed.description = f"**Owner**: {guild.owner.mention}\n**Categories**: {len(guild.categories)}\n**Text Channels**: {len(guild.text_channels)}\n**Voice Channels**: {len(guild.voice_channels)}\n**Members**: {guild.member_count - self.guild.bot_count} Users, {self.guild.bot_count} Bots"
        
        self.embed.set_author(name=guild.name, icon_url=guild.icon.url)
        self.embed.set_thumbnail(url=guild.icon.url)
        self.embed.set_footer(text=f"ID: {guild.id}")
        
        # self.console.clear_items()
        # self.console.add_item(self.console.party_button)
        # self.console.add_item(self.console.roles_button)
        # self.console.add_item(self.console.moderation_button)