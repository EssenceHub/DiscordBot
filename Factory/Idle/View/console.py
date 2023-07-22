import discord

class ConsoleUI(discord.ui.View):
    def __init__(self):
        super().__init__()

        # Embed
        self.embed = discord.Embed()

        # Buttons
        self.character_info_button = discord.ui.Button(label="Character", style=discord.ButtonStyle.blurple, row=1)
        self.dungeon_info_button = discord.ui.Button(label="Dungeon", style=discord.ButtonStyle.blurple, row=1)
        self.monster_summon_button = discord.ui.Button(label="Summon", style=discord.ButtonStyle.grey, row=1)
        self.character_creation_button = discord.ui.Button(label="Create Character", style=discord.ButtonStyle.green, row=1)
        self.dungeon_creation_button = discord.ui.Button(label="Create Dungeon", style=discord.ButtonStyle.green, row=1)
        self.summon_creation_button = discord.ui.Button(label="Create Summon", style=discord.ButtonStyle.green, row=1)
        
        # Modals
        self.modals = Modals()
        self.character_creation_modal = self.modals.Character_Creation_Modal()
        self.dungeon_creation_modal = self.modals.Dungeon_Creation_Modal()
        self.summon_creation_modal = self.modals.Summon_Creation_Modal()

        # Selections
        self.monster_summon_selection = discord.ui.Select(placeholder="Summon a Monster")

class Modals:
    def Character_Creation_Modal(self):
        modal = discord.ui.Modal(title="Create Character")

        character_name = discord.ui.TextInput(label="Character Name:")
        character_name.max_length = 32

        modal.add_item(character_name)
        return modal

    def Dungeon_Creation_Modal(self):
        modal = discord.ui.Modal(title="Create Dungeon")
        
        dungeon_name = discord.ui.TextInput(label="Dungeon Name:")
        dungeon_name.max_length = 32

        modal.add_item(dungeon_name)
        return modal

    def Summon_Creation_Modal(self):
        modal = discord.ui.Modal(title="Create Summon")
        
        summon_name = discord.ui.TextInput(label="Summon Name:")
        summon_name.max_length = 32

        number_input = discord.ui.TextInput(label="Summon Strength:")

        modal.add_item(summon_name)
        modal.add_item(number_input)
        return modal

# class Selections:
#     def Monster_Summon_Selection(self):
#         selection = discord.ui.Select()
#         monsters = self.
#         for monster in monsters:
#             option = discord.SelectOption(label=f"Monster {monster}", value=f"{monster}")
#             monsters.append(option)

#         selection.options = monsters
#         return selection
    
    