from Factory.Guild.View.console import ConsoleUI
from Factory.Guild.Controller.modifiers import ConsoleLogic
from Factory.Guild.Model.guild import Guild

class Callbacks:
    def __init__(self, console: ConsoleUI, guild: Guild):
        # UI
        self.console = console
        self.embed = console.embed

        # Guild
        self.member = guild
        self.interaction = guild.interaction
        

        # Database
        self.db = guild.db
        self.cursor = guild.cursor

        # Callbacks
        self.console_logic = ConsoleLogic(console, guild)