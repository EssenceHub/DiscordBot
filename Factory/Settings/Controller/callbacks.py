import discord

from datetime import timedelta

from Factory.Settings.View.console import ConsoleUI
from Factory.Settings.Controller.modifiers import ConsoleLogic
from Factory.Settings.Model.data import Data

class Callbacks:
    def __init__(self, data: Data):
        # UI
        self.console = ConsoleUI()
        self.embed = self.console.embed

        # Data
        self.data = data
        self.user = data.user
        self.interaction = data.interaction
        

        # Database
        self.db = data.db
        self.cursor = data.cursor

        # Button Callbacks
        self.console.settings_button.callback = self.Settings_Callback

        self.console.user_preferences_button.callback = self.User_Preferences_Callback
        self.console.server_configuration_button.callback = self.Server_Configuration_Callback

        self.console.notifications_button.callback = self.Notifications_Callback
        self.console.profile_visibility_button.callback = self.Profile_Visibility_Callback

        self.console.channels_button.callback = self.Channels_Callback
        self.console.commands_button.callback = self.Commands_Callback
        self.console.moderation_button.callback = self.Moderation_Callback
        self.console.roles_button.callback = self.Roles_Callback

        self.console.logs_button.callback = self.Logs_Callback
        self.console.inbox_button.callback = self.Inbox_Callback
        self.console.counting_button.callback = self.Counting_Callback
        self.console.truth_or_dare_button.callback = self.Truth_or_Dare_Callback
        self.console.two_word_story_button.callback = self.Two_Word_Story_Callback

        self.console.self_roles_button.callback = self.Self_Roles_Callback

        self.console.add_self_role_button.callback = self.Add_Self_Role_Callback
        self.console.remove_self_role_button.callback = self.Remove_Self_Role_Callback

        self.console.rewards_button.callback = self.Rewards_Callback

        self.console.add_reward_button.callback = self.Add_Reward_Callback
        self.console.remove_reward_button.callback = self.Remove_Reward_Callback

        self.console.punishment_edit_button.callback = self.Punishment_Edit_Callback

        # Modal Submissions
        self.console.logs_modal.on_submit = self.Logs_Submission
        self.console.inbox_modal.on_submit = self.Inbox_Submission
        self.console.counting_modal.on_submit = self.Counting_Submission
        self.console.truth_or_dare_modal.on_submit = self.Truth_or_Dare_Submission
        self.console.two_word_story_modal.on_submit = self.Two_Word_Story_Submission

        self.console.add_self_role_modal.on_submit = self.Add_Self_Role_Submission
        self.console.remove_self_role_modal.on_submit = self.Remove_Self_Role_Submission

        self.console.add_reward_modal.on_submit = self.Add_Reward_Submission
        self.console.remove_reward_modal.on_submit = self.Remove_Reward_Submission

        self.console.punishment_edit_modal.on_submit = self.Punishment_Edit_Submission

        self.console_logic = ConsoleLogic(self.console, data)

    # Buttons
    async def Settings_Callback(self, interaction: discord.Interaction):
        self.console_logic.Settings()

        await interaction.response.edit_message(embed=self.embed, view=self.console)
    


    async def User_Preferences_Callback(self, interaction: discord.Interaction):
        self.console_logic.User_Preferences()
        
        await interaction.response.edit_message(embed=self.embed, view=self.console)



    async def Server_Configuration_Callback(self, interaction: discord.Interaction):
        self.console_logic.Server_Configuration()
        
        await interaction.response.edit_message(embed=self.embed, view=self.console)
    


    async def Notifications_Callback(self, interaction: discord.Interaction):
        sql = "UPDATE EssenceUserData SET notifications = ? WHERE member_id = ? AND guild_id = ?"
        
        print(self.user.id, self.data.guild.id)
        if self.data.user_notifications:
            val = (0, interaction.user.id, interaction.guild.id)
            self.data.user_notifications = False

        else:
            val = (1, interaction.user.id, interaction.guild.id)
            self.data.user_notifications = True

        self.cursor.execute(sql, val)
        self.db.commit()

        self.console_logic.update_button_toggle_colors()
        self.console_logic.User_Preferences()
        
        await interaction.response.edit_message(embed=self.embed, view=self.console)



    async def Profile_Visibility_Callback(self, interaction: discord.Interaction):
        sql = "UPDATE EssenceUserData SET profile_visibility = ? WHERE member_id = ? AND guild_id = ?"
        
        if self.data.user_profile_visibility:
            val = (0, self.user.id, self.data.guild.id)
            self.data.user_profile_visibility = False

        else:
            val = (1, self.user.id, self.data.guild.id)
            self.data.user_profile_visibility = True

        self.cursor.execute(sql, val)
        self.db.commit()

        self.console_logic.update_button_toggle_colors()
        self.console_logic.User_Preferences()
        
        await interaction.response.edit_message(embed=self.embed, view=self.console)
    


    async def Channels_Callback(self, interaction: discord.Interaction):
        self.console_logic.Channel_Configuration()
        
        await interaction.response.edit_message(embed=self.embed, view=self.console)



    async def Commands_Callback(self, interaction: discord.Interaction):
        self.console_logic.Commands_Explanation()
        
        await interaction.response.edit_message(embed=self.embed, view=self.console)



    async def Moderation_Callback(self, interaction: discord.Interaction):
        self.console_logic.Moderation()
        
        await interaction.response.edit_message(embed=self.embed, view=self.console)

    async def Roles_Callback(self, interaction: discord.Interaction):
        self.console_logic.Roles()
        
        await interaction.response.edit_message(embed=self.embed, view=self.console)



    async def Self_Roles_Callback(self, interaction: discord.Interaction):
        self.console_logic.Self_Roles()
        
        await interaction.response.edit_message(embed=self.embed, view=self.console)



    async def Rewards_Callback(self, interaction: discord.Interaction):
        self.console_logic.Role_Rewards()
        
        await interaction.response.edit_message(embed=self.embed, view=self.console)
    


    async def Logs_Callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(self.console.logs_modal)



    async def Inbox_Callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(self.console.inbox_modal)
        


    async def Counting_Callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(self.console.counting_modal)
        


    async def Truth_or_Dare_Callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(self.console.truth_or_dare_modal)
        


    async def Two_Word_Story_Callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(self.console.two_word_story_modal)
    


    async def Add_Self_Role_Callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(self.console.add_self_role_modal)



    async def Remove_Self_Role_Callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(self.console.remove_self_role_modal)
    


    async def Add_Reward_Callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(self.console.add_reward_modal)



    async def Remove_Reward_Callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(self.console.remove_reward_modal)
    


    async def Punishment_Edit_Callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(self.console.punishment_edit_modal)



    # Modals
    async def Logs_Submission(self, interaction: discord.Interaction):
        id = interaction.data["components"][0]["components"][0]["value"]
        try:
            id = int(id)
            logs_channel = interaction.guild.get_channel(id)
            if logs_channel is None:
                raise Exception
        except ValueError:
            await interaction.response.send_message("That is not a valid channel id", ephemeral=True)
            return
        
        sql = "UPDATE EssenceGuildData SET logs_id = ? WHERE guild_id = ?"
        val = (id, interaction.guild.id)

        self.cursor.execute(sql, val)
        self.db.commit()

        self.console_logic.Channel_Updated("Logs Channel Updated", logs_channel.id)
        await interaction.response.edit_message(embed=self.embed, view=self.console)



    async def Inbox_Submission(self, interaction: discord.Interaction):
        id = interaction.data["components"][0]["components"][0]["value"]
        try:
            id = int(id)
            inbox_channel = interaction.guild.get_channel(id)
            if inbox_channel is None:
                raise Exception
        except ValueError:
            await interaction.response.send_message("That is not a valid channel id", ephemeral=True)
            return
        
        sql = "UPDATE EssenceGuildData SET mail_id = ? WHERE guild_id = ?"
        val = (id, interaction.guild.id)

        self.cursor.execute(sql, val)
        self.db.commit()

        self.console_logic.Channel_Updated("Inbox Channel Updated", inbox_channel.id)
        await interaction.response.edit_message(embed=self.embed, view=self.console)
        


    async def Counting_Submission(self, interaction: discord.Interaction):
        id = interaction.data["components"][0]["components"][0]["value"]
        try:
            id = int(id)
            counting_channel = interaction.guild.get_channel(id)
            if counting_channel is None:
                raise Exception
        except ValueError:
            await interaction.response.send_message("That is not a valid channel id", ephemeral=True)
            return
        
        sql = "UPDATE EssenceGuildData SET counting_id = ? WHERE guild_id = ?"
        val = (id, interaction.guild.id)

        self.cursor.execute(sql, val)
        self.db.commit()

        self.console_logic.Channel_Updated("Counting Channel Updated", counting_channel.id)
        await interaction.response.edit_message(embed=self.embed, view=self.console)
        


    async def Truth_or_Dare_Submission(self, interaction: discord.Interaction):
        id = interaction.data["components"][0]["components"][0]["value"]
        try:
            id = int(id)
            truth_or_dare_channel = interaction.guild.get_channel(id)
            if truth_or_dare_channel is None:
                raise Exception
        except ValueError:
            await interaction.response.send_message("That is not a valid channel id", ephemeral=True)
            return
        
        sql = "UPDATE EssenceGuildData SET tod_id = ? WHERE guild_id = ?"
        val = (id, interaction.guild.id)

        self.cursor.execute(sql, val)
        self.db.commit()

        self.console_logic.Channel_Updated("Truth or Dare Channel Updated", truth_or_dare_channel.id)
        await interaction.response.edit_message(embed=self.embed, view=self.console)
        


    async def Two_Word_Story_Submission(self, interaction: discord.Interaction):
        id = interaction.data["components"][0]["components"][0]["value"]
        try:
            id = int(id)
            two_word_story_channel = interaction.guild.get_channel(id)
            if two_word_story_channel is None:
                raise Exception
        except ValueError:
            await interaction.response.send_message("That is not a valid channel id", ephemeral=True)
            return
        
        sql = "UPDATE EssenceGuildData SET tws_id = ? WHERE guild_id = ?"
        val = (id, interaction.guild.id)

        self.cursor.execute(sql, val)
        self.db.commit()

        self.console_logic.Channel_Updated("Two Word Story Channel Updated", two_word_story_channel.id)
        await interaction.response.edit_message(embed=self.embed, view=self.console)
    


    async def Add_Self_Role_Submission(self, interaction: discord.Interaction):
        id = interaction.data["components"][0]["components"][0]["value"]
        desc = interaction.data["components"][1]["components"][0]["value"]

        try:
            role = interaction.guild.get_role(int(id))
            if role == None:
                raise ValueError

        except ValueError:
            interaction.response.send_message("That is not a valid role id", ephemeral=True)
            return

        sql = "INSERT INTO EssenceRoleData(role_id, guild_id, description, self_assignable) VALUES (?, ?, ?, ?)"
        val = (id, interaction.guild.id, desc, 1)
        self.cursor.execute(sql, val)
        self.db.commit()

        self.console_logic.Self_Role_Added(role)
        await interaction.response.edit_message(embed=self.embed, view=self.console)


    async def Remove_Self_Role_Submission(self, interaction: discord.Interaction):
        id = interaction.data["components"][0]["components"][0]["value"]

        try:
            role = interaction.guild.get_role(int(id))
            if role == None:
                raise ValueError

        except ValueError:
            interaction.response.send_message("That is not a valid role id", ephemeral=True)
            return

        sql = "DELETE FROM EssenceRoleData WHERE role_id = ? AND guild_id = ? AND self_assignable = ?"
        val = (id, interaction.guild.id, 1)
        self.cursor.execute(sql, val)
        self.db.commit()

        self.console_logic.Self_Role_Removed(role)
        await interaction.response.edit_message(embed=self.embed, view=self.console)




    async def Add_Reward_Submission(self, interaction: discord.Interaction):
        id = interaction.data["components"][0]["components"][0]["value"]
        requirement = interaction.data["components"][1]["components"][0]["value"]

        try:
            role = interaction.guild.get_role(int(id))
            if role == None:
                raise ValueError

        except ValueError:
            interaction.response.send_message("That is not a valid role id", ephemeral=True)
            return

        try:
            requirement = int(requirement)

        except ValueError:
            await interaction.response.send_message("That is not a valid activity point requirement", ephemeral=True)
            return

        sql = "INSERT INTO EssenceRoleData(role_id, guild_id, requirement, self_assignable) VALUES (?, ?, ?, ?)"
        val = (role.id, interaction.guild.id, requirement, 0)
        self.cursor.execute(sql, val)
        self.db.commit()

        self.console_logic.Role_Added(role, requirement)
        await interaction.response.edit_message(embed=self.embed, view=self.console)



    async def Remove_Reward_Submission(self, interaction: discord.Interaction):
        id = interaction.data["components"][0]["components"][0]["value"]

        try:
            id = int(id)

            role = interaction.guild.get_role(id)
            if role == None:
                raise ValueError

        except ValueError:
            await interaction.response.send_message("That is not a valid role id", ephemeral=True)
            return

        sql = "DELETE FROM EssenceRoleData WHERE role_id = ? AND guild_id = ?"
        val = (role.id, interaction.guild.id)
        self.cursor.execute(sql, val)
        self.db.commit()

        self.console_logic.Role_Removed(role)
        await interaction.response.edit_message(embed=self.embed, view=self.console)
    


    async def Punishment_Edit_Submission(self, interaction: discord.Interaction):
        number = interaction.data["components"][0]["components"][0]["value"]
        type = str.lower(interaction.data["components"][1]["components"][0]["value"])
        length = str.lower(interaction.data["components"][2]["components"][0]["value"])
        
        try:
            number = int(number)
        except ValueError:
            await interaction.response.send_message("That is not a valid punishment number", ephemeral=True)
            return

        if not number in [1, 2, 3, 4, 5]:
            await interaction.response.send_message("That is not a valid punishment number", ephemeral=True)
            return

        if not type in ["warn", "timeout", "ban"]:
            await interaction.response.send_message("That is not a valid punishment type", ephemeral=True)
            return
        
        try:
            if length != '':
                print(length)
                amount = ''
                letter = ''
                for character in length:
                    if str.isdigit(character):
                        amount = amount + character
                    else:
                        letter = character

                amount = int(amount)

                if letter == "h":
                    timedelta(hours=amount)
                elif letter == "d":
                    timedelta(days=amount)
                elif letter == "w":
                    timedelta(weeks=amount)
        except:
            await interaction.response.send_message("That is not a valid punishment length", ephemeral=True)
            return
        
        sql = f"UPDATE EssenceGuildData SET punishment{number} = ? WHERE guild_id = ?"
        
        if type == "timeout":
            val = (type+length, interaction.guild.id)
        else:
            val = (type, interaction.guild.id)

        self.cursor.execute(sql, val)
        self.db.commit()

        self.console_logic.Punishment_Updated(interaction)
        await interaction.response.edit_message(embed=self.embed, view=self.console)