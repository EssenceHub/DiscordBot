from Factory.Idle.View.console import ConsoleUI 
from Factory.Idle.Model.player import Player 
from Factory.Idle.Controller.monsters import Monsters 
# Type hinting ^^

class ConsoleLogic():
    def __init__(self, console: ConsoleUI, player: Player, monsters: Monsters):
        # Inheritance
        self.console = console
        self.player = player
        self.embed = console.embed
        self.interaction = player.interaction
        self.monsters = monsters

        self.Starter_Console()

    # Console Logic
    def Starter_Console(self):
        self.embed.title = ""
        self.embed.description = ""

        if self.player.stored_id is None: 
            self.player.cursor.execute(f"INSERT INTO EssenceIdleData(member_id) VALUES ({self.player.id})")
            self.player.db.commit()

        # Brings up the character info console for the user
        self.Character_Info_Console()
    




    def Character_Info_Console(self):
        # Brings up the character creation console for the user
        if self.player.character_name is None:
            self.Character_Creation_Console()
            return

        self.embed.title       = self.player.character_name
        self.embed.description = f"""
            **Level:** {self.player.character_level}
            
            **--- Skills ---**
            [Dungeon Architect]: {self.player.dungeons}/1 Dungeons Built
            [Breath of Life]: {len(self.monsters.monster_options)}/25 Monsters Born
            [Summon]: Summon a monster you've created.
            """ # Show 1/1 Dungeons created for dungeon creation and put the name, then for monster summon it should be dynamic #/6 for all the different options of creating monsters
    
        self.console.clear_items()
        self.console.add_item(self.console.dungeon_info_button)



    def Dungeon_Info_Console(self):
        if self.player.dungeon_name is None: 
            # Brings up the dungeon creation console for the user
            self.Dungeon_Creation_Console()
            return

        # This function updates the dungeon's stats
        self.player.update_dungeon()

        self.embed.title       = f"{self.player.dungeon_name}"
        self.embed.description = f"""
            **Power:** {self.player.dungeon_power}
            **Energy:** {self.player.dungeon_energy}
            """
        
        self.console.clear_items()
        self.console.add_item(self.console.character_info_button)
        self.console.add_item(self.console.monster_summon_button)



    def Character_Creation_Console(self):
        self.embed.title       = "Character Creation"
        self.embed.description = f"Name your character, choose a custom name or just use your discord name ({self.interaction.user.name})."

        self.console.clear_items()
        self.console.add_item(self.console.character_creation_button)
    


    def Character_Created_Console(self):
        self.embed.title       = "Character Created"
        self.embed.description = f"{self.player.character_name} has been born, while others are able to bend elements to their will and make object's float with their minds... {self.player.character_name} can create a dungeon, and summon monsters."

        self.console.clear_items()
        self.console.add_item(self.console.character_info_button)
        self.console.add_item(self.console.dungeon_creation_button)



    def Dungeon_Creation_Console(self):
        self.embed.title       = "Dungeon Creation"
        self.embed.description = f"{self.player.character_name}'s power comes not from themselves, but what they can create. {self.player.character_name} want's to create their first dungeon but... what should the dungeon's name be?"
        
        self.console.clear_items()
        self.console.add_item(self.console.character_info_button)
        self.console.add_item(self.console.dungeon_creation_button)
    


    def Dungeon_Created_Console(self):
        self.embed.title       = "Dungeon Created"
        self.embed.description = "Another dungeon has appeared in the world, nobody knows anything about it but will send people to check on it... just in case."
        
        self.console.clear_items()
        self.console.add_item(self.console.dungeon_info_button)



    def Dungeon_Summon_Console(self):
        # Updates the monster summon options every time the summon console is instantiated
        self.console.monster_summon_selection.options = self.monsters.monster_options

        self.embed.title       = "Summon Monsters"
        self.embed.description = "Consume energy to summon one of your monsters for your dungeon"
        
        self.console.clear_items()
        self.console.add_item(self.console.monster_summon_selection)
        self.console.add_item(self.console.dungeon_info_button)
        self.console.add_item(self.console.summon_creation_button)



    def Monster_Summon_Console(self, summon_price: int):
        self.embed.title       = "Monster Summon"
        self.embed.description = self.player.increase_dungeon_power(summon_price)


    
    def Summon_Creation_Console(self):
        self.embed.title       = "Create a Summon"
        self.embed.description = f"{self.player.character_name} can breathe life into a species of monster and then summon them to protect their dungeon, what should {self.player.character_name} name it?"

        self.console.clear_items()
        self.console.add_item(self.console.dungeon_info_button)
        self.console.add_item(self.console.summon_creation_button)


    
    def Summon_Created_Console(self):
        self.embed.title       = "Summon Created"
        self.embed.description = f"{self.player.character_name} has created a new species of summon called {self.monsters.creation_name}"

        self.console.clear_items()
        self.console.add_item(self.console.dungeon_info_button)
        self.console.add_item(self.console.summon_creation_button)
    


    def Summon_Error_Console(self):
        self.embed.title       = "Pressure"
        self.embed.description = f"{self.player.character_name} feels a strong resistance when creating another summon."

        self.console.clear_items()
        self.console.add_item(self.console.dungeon_info_button)