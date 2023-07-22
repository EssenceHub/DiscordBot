import discord

class ConsoleUI(discord.ui.View):
    def __init__(self):
        super().__init__()

        # Embed
        self.embed = discord.Embed()
        self.embed.color = 0x800080

        # Settings Buttons
        self.settings_button = discord.ui.Button(label="Settings", style=discord.ButtonStyle.blurple, row=3)
        self.user_preferences_button = discord.ui.Button(label="User Preferences", style=discord.ButtonStyle.blurple, row=3)
        self.server_configuration_button = discord.ui.Button(label="Server Configuration", style=discord.ButtonStyle.blurple, row=3)

        # User Preferences Buttons
        self.notifications_button = discord.ui.Button(label="Notifications", style=discord.ButtonStyle.grey, row=1)
        self.profile_visibility_button = discord.ui.Button(label="Profile Visibility", style=discord.ButtonStyle.grey, row=1)

        # Server Configuration Buttons
        self.channels_button = discord.ui.Button(label="Channels", style=discord.ButtonStyle.grey, row=2)
        self.commands_button = discord.ui.Button(label="Commands", style=discord.ButtonStyle.grey, row=2)
        self.moderation_button = discord.ui.Button(label="Moderation", style=discord.ButtonStyle.grey, row=2)
        self.roles_button = discord.ui.Button(label="Roles", style=discord.ButtonStyle.grey, row=2)

        # Channels Buttons
        self.logs_button = discord.ui.Button(label="Logs", style=discord.ButtonStyle.grey, row=1)
        self.inbox_button = discord.ui.Button(label="Inbox", style=discord.ButtonStyle.grey, row=1)
        self.counting_button = discord.ui.Button(label="Counting", style=discord.ButtonStyle.green, row=1)
        self.truth_or_dare_button = discord.ui.Button(label="Truth or Dare", style=discord.ButtonStyle.green, row=1)
        self.two_word_story_button = discord.ui.Button(label="Two Word Story", style=discord.ButtonStyle.green, row=1)

        # Moderation Buttons
        self.punishment_edit_button = discord.ui.Button(label="Edit Punishments", style=discord.ButtonStyle.grey, row=1)

        # Role Buttons
        self.rewards_button = discord.ui.Button(label="Reward Roles", style=discord.ButtonStyle.grey, row=1)
        self.self_roles_button = discord.ui.Button(label="Self Roles", style=discord.ButtonStyle.grey, row=1)

        # Rewards Buttons
        self.add_reward_button = discord.ui.Button(label="Add Reward", style=discord.ButtonStyle.green, row=1)
        self.remove_reward_button = discord.ui.Button(label="Remove Reward", style=discord.ButtonStyle.red, row=1)

        # Rewards Buttons
        self.add_self_role_button = discord.ui.Button(label="Add Role", style=discord.ButtonStyle.green, row=1)
        self.remove_self_role_button = discord.ui.Button(label="Remove Role", style=discord.ButtonStyle.red, row=1)

        # Modals
        self.modals = Modals()

        # Channel Modals
        self.logs_modal = self.modals.Logs_Modal()
        self.inbox_modal = self.modals.Inbox_Modal()
        self.counting_modal = self.modals.Counting_Modal()
        self.truth_or_dare_modal = self.modals.Truth_or_Dare_Modal()
        self.two_word_story_modal = self.modals.Two_Word_Story_Modal()
        
        # Self Role Modals
        self.add_self_role_modal = self.modals.Add_Self_Role_Modal()
        self.remove_self_role_modal = self.modals.Remove_Self_Role_Modal()
        
        # Reward Role Modals
        self.add_reward_modal = self.modals.Add_Reward_Modal()
        self.remove_reward_modal = self.modals.Remove_Reward_Modal()
        
        # Moderation Modals
        self.punishment_edit_modal = self.modals.Punishment_Edit_Modal()

class Modals:
    def Logs_Modal(self):
        modal = discord.ui.Modal(title="Set Logs ID")

        logs_id = discord.ui.TextInput(label="Channel ID:")
        logs_id.max_length = 20

        modal.add_item(logs_id)
        return modal
        
    def Inbox_Modal(self):
        modal = discord.ui.Modal(title="Set Inbox ID")

        inbox_id = discord.ui.TextInput(label="Channel ID:")
        inbox_id.max_length = 20

        modal.add_item(inbox_id)
        return modal
        
    def Counting_Modal(self):
        modal = discord.ui.Modal(title="Set Counting ID")

        counting_id = discord.ui.TextInput(label="Channel ID:")
        counting_id.max_length = 20

        modal.add_item(counting_id)
        return modal
        
    def Truth_or_Dare_Modal(self):
        modal = discord.ui.Modal(title="Set Truth or Dare ID")

        truth_or_dare_id = discord.ui.TextInput(label="Channel ID:")
        truth_or_dare_id.max_length = 20

        modal.add_item(truth_or_dare_id)
        return modal
        
    def Two_Word_Story_Modal(self):
        modal = discord.ui.Modal(title="Set Two Word Story ID")

        two_word_story_id = discord.ui.TextInput(label="Channel ID:")
        two_word_story_id.max_length = 20

        modal.add_item(two_word_story_id)
        return modal

    def Add_Self_Role_Modal(self):
        modal = discord.ui.Modal(title="Add Self Assignable Role")

        role_id = discord.ui.TextInput(label="Role ID:")
        role_id.placeholder = "ID..."

        role_desc = discord.ui.TextInput(label="Role Description:")
        role_desc.placeholder = "..."

        modal.add_item(role_id)
        modal.add_item(role_desc)
        return modal

    def Remove_Self_Role_Modal(self):
        modal = discord.ui.Modal(title="Remove Self Assignable Role")

        role_id = discord.ui.TextInput(label="Role ID:")
        role_id.placeholder = "ID..."

        modal.add_item(role_id)
        return modal

    def Add_Reward_Modal(self):
        modal = discord.ui.Modal(title="Add Reward to Role")

        role_id = discord.ui.TextInput(label="Role ID:")
        role_id.placeholder = "ID..."

        role_requiurement = discord.ui.TextInput(label="Requirement:")
        role_requiurement.placeholder = "..."

        modal.add_item(role_id)
        modal.add_item(role_requiurement)
        return modal

    def Remove_Reward_Modal(self):
        modal = discord.ui.Modal(title="Remove Reward from Role")

        role_id = discord.ui.TextInput(label="Role ID:")
        role_id.placeholder = "ID..."

        modal.add_item(role_id)
        return modal
        
    def Punishment_Edit_Modal(self):
        modal = discord.ui.Modal(title="Edit Punishments")

        punishment_number = discord.ui.TextInput(label="Punishment Number:")
        punishment_number.placeholder = "1-5..."
        punishment_number.max_length = 1

        punishment_type = discord.ui.TextInput(label="Punishment Type:")
        punishment_type.placeholder = "warn/timeout/ban..."
        punishment_type.max_length = 8

        punishment_length = discord.ui.TextInput(label="Punishment Length:")
        punishment_length.placeholder = "6h/3d/1w... (timeouts only)"
        punishment_length.max_length = 8
        punishment_length.required = False

        modal.add_item(punishment_number)
        modal.add_item(punishment_type)
        modal.add_item(punishment_length)
        return modal