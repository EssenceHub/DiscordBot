import discord

from Factory.Settings.View.console import ConsoleUI
from Factory.Settings.Model.data import Data

class ConsoleLogic:
    def __init__(self, console: ConsoleUI, data: Data):
        # UI
        self.console = console
        self.embed = console.embed

        # Data
        self.data = data
        self.guild = data.guild
        self.user = data.user

        self.Settings()

    # Console Logic
    def Settings(self):
        self.embed.title = "Settings"
        self.embed.description = "**User Preferences**:\nNotifications | Profile Visibility\n\n**Server Configuration**\nChannels | Commands | Moderation | Roles"

        self.console.clear_items()
        self.console.add_item(self.console.user_preferences_button)
        self.console.add_item(self.console.server_configuration_button)

    # User preferences function
    def User_Preferences(self):
        self.embed.title = "User Preferences"
        self.embed.description = f"**Toggles:**\nNotifications: {self.data.get_preference_emoji(self.data.user_notifications)}\nProfile Visibility: {self.data.get_preference_emoji(self.data.user_profile_visibility)}"

        self.console.clear_items()
        self.update_button_toggle_colors()
        self.console.add_item(self.console.notifications_button)
        self.console.add_item(self.console.profile_visibility_button)

        if self.user.guild_permissions.manage_guild:
            self.console.add_item(self.console.settings_button)

    # Server configuration functions
    def Server_Configuration(self):
        self.embed.title = "Server Configuration"
        self.embed.description = f"**Information:**\n**Channels:** Set the channel id of your logs, inbox and game channels\n**Commands:** How to configure where and who can use certain commands\n**Moderation:** Modify the punishments users get when punished\n**Roles:** Give roles when users get a certain amount of activity points or allow them to assign roles to themselves!"

        self.console.clear_items()
        self.console.add_item(self.console.channels_button)
        self.console.add_item(self.console.commands_button)
        self.console.add_item(self.console.moderation_button)
        self.console.add_item(self.console.roles_button)
        
        self.console.add_item(self.console.settings_button)

    def Channel_Configuration(self):
        self.embed.title = "Channel Configuration"
        self.embed.description = "**Logs:** All user messages, edits and delete will be posted in this channel\n**Inbox:** All user suggestions and report will be posted in this channel\n**Counting:** Specifies a channel to give the rules of the counting game\n**Truth or Dare:** Specifies the channel to give the rules of truth or dare\n**Two Word Story:** Specifies the channel to give the rules of two word story"

        self.console.clear_items()
        self.console.add_item(self.console.logs_button)
        self.console.add_item(self.console.inbox_button)
        self.console.add_item(self.console.counting_button)
        self.console.add_item(self.console.truth_or_dare_button)
        self.console.add_item(self.console.two_word_story_button)
        
        self.console.add_item(self.console.server_configuration_button)

    def Commands_Explanation(self):
        self.embed.title = "How to configure command permissions"
        self.embed.description = '1. Open Server Settings\n2. Open Integrations in the APPS category\n3. Scroll down to Essence and click "Manage"\n4. Configure'

        self.console.clear_items()
        
        self.console.add_item(self.console.server_configuration_button)

    def Moderation(self):
        self.embed.title = "Punishment System"
        self.embed.description = f"Essence's punishments system is a 5 strike system where the user gets increasingly strict punishments each time, you can edit these punishments with the button below.\n\n**Current Punishments:**\n{self.data.get_punishment_data()}"

        self.console.clear_items()
        self.console.add_item(self.console.punishment_edit_button)
        
        self.console.add_item(self.console.server_configuration_button)

    def Roles(self):
        self.embed.title = "Role Configuration"
        self.embed.description = f"Essence was built to make role assignment simpler, here you can add activity reward roles and self assignable roles."

        self.console.clear_items()
        self.console.add_item(self.console.self_roles_button)
        self.console.add_item(self.console.rewards_button)
        
        self.console.add_item(self.console.server_configuration_button)

    def Channel_Updated(self, title: str, channel: discord.channel.TextChannel):
        self.embed.title = title
        self.embed.description = f"{title} to <#{channel}>"

        self.console.clear_items()
        self.console.add_item(self.console.channels_button)
    
    def Punishment_Updated(self, interaction: discord.Interaction):
        number = interaction.data["components"][0]["components"][0]["value"]
        type = interaction.data["components"][1]["components"][0]["value"]
        length = interaction.data["components"][2]["components"][0]["value"]

        self.embed.title = f"Punishment Number {number} Updated"
        self.embed.description = f"Punishment number {number} has been updated to {type+length}"

        self.console.clear_items()
        self.console.add_item(self.console.moderation_button)

    def Self_Roles(self):
        self.embed.title = "Self Roles"
        if self.data.reward_str == "**Achievable Roles:**":
            self.embed.description = f"Add or remove roles to the self role command\n\n{self.data.self_role_str}"
        else:
            self.embed.description = f"Add or remove roles to the self role command"
            

        self.console.clear_items()
        self.console.add_item(self.console.add_self_role_button)
        self.console.add_item(self.console.remove_self_role_button)
        
        self.console.add_item(self.console.roles_button)

    def Role_Rewards(self):
        self.embed.title = "Activity Role Rewards"
        if self.data.reward_str == "**Achievable Roles:**":
            self.embed.description = "Add rewards for activity to roles. You have to remove a reward from a role before you can reassign a new reward requirement to it!"
        else:
            self.embed.description = f"Add rewards for activity to roles. You have to remove a reward from a role before you can reassign a new reward requirement to it!\n\n{self.data.reward_str}"

        self.console.clear_items()
        self.console.add_item(self.console.add_reward_button)
        self.console.add_item(self.console.remove_reward_button)
        
        self.console.add_item(self.console.roles_button)
        
    def Self_Role_Added(self, role: discord.Role):
        self.embed.title = f"Self Role Created"
        self.embed.description = f"{role.mention} is now selectable by users through the /roles command!"

        self.console.clear_items()
        self.console.add_item(self.console.roles_button)
        
    def Self_Role_Removed(self, role: discord.Role):
        self.embed.title = f"Self Role Deleted"
        self.embed.description = f"{role.mention} is no longer selectable by users through the /roles command!"

        self.console.clear_items()
        self.console.add_item(self.console.roles_button)
    
    def Role_Added(self, role: discord.Role, requirement: int):
        self.embed.title = f"Activity Reward Role Created"
        self.embed.description = f"{role.mention} is now achievable by users through sending messages and participating in voice chats and getting {requirement} activity points!"

        self.console.clear_items()
        self.console.add_item(self.console.rewards_button)
    
    def Role_Removed(self, role: discord.Role):
        self.embed.title = f"Activity Reward Role Removed"
        self.embed.description = f"{role.mention} is no longer achievable by users through sending messages and participating in voice chats."

        self.console.clear_items()
        self.console.add_item(self.console.rewards_button)
    



    # Utils
    def update_button_toggle_colors(self):
        # User notifications
        if self.data.user_notifications:
            self.console.notifications_button.style = discord.ButtonStyle.green
        else:
            self.console.notifications_button.style = discord.ButtonStyle.red

        # Profile Visibility
        if self.data.user_profile_visibility:
            self.console.profile_visibility_button.style = discord.ButtonStyle.green
        else:
            self.console.profile_visibility_button.style = discord.ButtonStyle.red

