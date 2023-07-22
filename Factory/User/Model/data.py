import discord
import sqlite3

from Factory.utils import capitalize_words
from operator import itemgetter

class Data():
    def __init__(self, interaction: discord.Interaction, user: discord.Member = None):
        self.interaction = interaction
        self.guild = interaction.guild

        self.db = sqlite3.connect("essence.db")
        self.cursor = self.db.cursor()

        self.get_user(user)
        self.get_user_data()
        self.get_activity_str()

    def get_user(self, user: discord.Member):
        if user == None:
            self.user = self.interaction.user
        else:
            self.user = user

    def get_user_data(self):
        self.cursor.execute(f'SELECT activity_points, party, party_rank, party_points FROM EssenceUserData WHERE guild_id = ? AND member_id = ?', (self.guild.id, self.user.id))
        self.activity_points, self.party, self.party_rank, self.party_points = self.cursor.fetchone() or (None, None, None, None)

        self.roles = self.get_user_roles()
        self.permissions = self.get_user_permissions()

    def get_user_roles(self):
        role_str = ""

        roles = self.user.roles
        for role in roles:
            if role.name != "@everyone":
                role_str = f"{role.mention} {role_str}"

        return role_str

    def get_user_permissions(self):
        permissions = self.user.guild_permissions
        user_permissions = ""

        for permission, value in permissions:
            if value:
                permission = permission.replace("_", " ").capitalize()
                permission = capitalize_words(permission)
                user_permissions += f"{permission}, "

        return user_permissions[:-2]
    
    def get_activity_str(self):
        # SQL Query
        sql = "SELECT role_id, requirement FROM EssenceRoleData WHERE guild_id = ? AND self_assignable != ?"
        val = (self.guild.id, 1)

        # SQL Execution
        self.cursor.execute(sql, val)
        reward_roles = self.cursor.fetchall()
        reward_roles.sort(key=itemgetter(1))

        # String builder
        for id, requirement in reward_roles:
            if self.activity_points < requirement:
                
                role =  self.guild.get_role(id)
                self.activity_str = f"{self.user.name} needs *{requirement - self.activity_points}* more activity points to reach the next milestone role, {role.mention}."
                return

        self.activity_str = f"{self.user.name} has *{self.activity_points}* activity points."
        return