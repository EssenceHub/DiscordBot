import discord

from Factory.Idle.Model.player import Player

class Monsters:
    def __init__(self, player: Player):
        self.monster_dict = self.convert_str_to_dict(player.dungeon_monsters)
        self.monster_str = self.convert_dict_to_str(self.monster_dict)
        self.monster_options = self.convert_dict_to_options(self.monster_dict)

        # Data
        self.player = player
        self.db = player.db
        self.cursor = player.cursor

    def convert_dict_to_options(self, monster_dict: dict or None):
        if monster_dict is None:
            return []
        
        monsters = []
        for monster in monster_dict:
            monster_value = monster_dict[monster]['Strength']
            monsters.append(discord.SelectOption(label=f"{monster} | Energy: {monster_value}", value=monster_value))
        return monsters

    def convert_str_to_dict(self, monster_str: str or None):
        if monster_str is None:
            return {}

        monsters = {}

        monster_str = monster_str.split("|")
        for monster in monster_str:
            monster_data = monster.split("-")

            # [Name, Level, Strength]
            monsters[monster_data[0]] = {"Level": monster_data[1], "Strength": monster_data[2]}
        return monsters
    
    def convert_dict_to_str(self, monster_dict: dict or None):
        if monster_dict == None:
            return ""
            
        monster_str = ""

        for monster in monster_dict.keys():
            monster_str = f"{monster_str}|{monster}-{monster_dict[monster]['Level']}-{monster_dict[monster]['Strength']}"
        monster_str = monster_str[1:]
        
        return monster_str

    def create(self, name: str, strength: int):
        self.creation = f"{name}-1-{strength}"

        if self.monster_str == "":
            self.monster_str = self.creation
        else:
            self.monster_str = f"{self.monster_str}|{self.creation}"

        self.cursor.execute(f"UPDATE EssenceIdleData SET dungeon_monsters = ? WHERE member_id = ?", (self.monster_str, self.player.id))
        self.db.commit()

        # Updates the other monster values
        self.monster_dict = self.convert_str_to_dict(self.monster_str)
        self.monster_options = self.convert_dict_to_options(self.monster_dict)
        self.creation_name = self.creation.split("-")[:-2]; self.creation_name = self.creation_name[0]

    def levelup(self, name: str):
        pass

    def eradicate(self, name: str):
        pass

# Give the users the ability to create their own monsters

# Save all monsters as a string inside of the database

# How to store data?

# N-L-S|N-L-S|N-L-S|N-L-S|
# Name-Level-Strength
# a-1-1|b-1-10|c-1-100|d-1-1000|e-1-10000