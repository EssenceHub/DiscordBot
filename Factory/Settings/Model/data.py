import discord
import sqlite3

from operator import itemgetter

class Data():
    def __init__(self, interaction: discord.Interaction):
        self.interaction = interaction
        self.guild = interaction.guild
        self.user = interaction.user

        self.db = sqlite3.connect("essence.db")
        self.cursor = self.db.cursor()

        self.get_user_preferences()
        self.get_reward_str()
        self.get_self_role_str()

    def get_user_preferences(self):
        self.cursor.execute("SELECT notifications, profile_visibility FROM EssenceUserData WHERE member_id = ? AND guild_id = ?", (self.user.id, self.guild.id))
        user_notifications, user_profile_visibility = self.cursor.fetchone()

        if user_notifications == 1:
            self.user_notifications = True
        else:
            self.user_notifications = False
        
        if user_profile_visibility == 1:
            self.user_profile_visibility = True
        else:
            self.user_profile_visibility = False

    def get_preference_emoji(self, input):
        if input:
            return "✅"
        else:
            return "❌"

    def get_punishment_data(self):
        self.cursor.execute("SELECT punishment1, punishment2, punishment3, punishment4, punishment5 FROM EssenceGuildData WHERE guild_id = ?", (self.guild.id,))
        stored_punishments = self.cursor.fetchone()

        punishments = {
            1: stored_punishments[0] or "warn (default)",
            2: stored_punishments[1] or "warn (default)",
            3: stored_punishments[2] or "timeout3d (default)",
            4: stored_punishments[3] or "timeout1w (default)",
            5: stored_punishments[4] or "ban (default)"
        }
        
        punishments = f"{punishments[1]}\n{punishments[2]}\n{punishments[3]}\n{punishments[4]}\n{punishments[5]}"
        return punishments

    def get_reward_str(self):
        # SQL Query
        sql = "SELECT role_id, requirement FROM EssenceRoleData WHERE guild_id = ? AND self_assignable != ?"
        val = (self.guild.id, 1)

        # SQL Execution
        self.cursor.execute(sql, val)
        reward_roles = self.cursor.fetchall()
        reward_roles.sort(key=itemgetter(1), reverse=True)

        # String builder
        self.reward_str = "**Achieveable Roles:**"
        for id, requirement in reward_roles:
            role = self.guild.get_role(id)
            self.reward_str = f"{self.reward_str}\n{role.mention} ID: {id} **for** {requirement} activity points"

    def get_self_role_str(self):
        # SQL Query
        sql = "SELECT role_id, description FROM EssenceRoleData WHERE guild_id = ? AND self_assignable = ?"
        val = (self.guild.id, 1)

        # SQL Execution
        self.cursor.execute(sql, val)
        self_roles = self.cursor.fetchall()

        # String builder
        self.self_role_str = "**Self Roles Available:**"
        for role_id, role_desc in self_roles:
            role = self.guild.get_role(role_id)
            self.self_role_str = f"{self.self_role_str}\n{role.mention}: {role_desc}"