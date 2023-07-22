import discord

from discord import app_commands
from discord.ext import commands

def get_prompt_descriptions():
    prompt_descriptions = {"kotw": "The knights of the week button opens a leaderboard where players can compete for ranks, among which players can be ranked for being aggresive, robbed, apocalyptic and fanatic.",
    "apoc timer": "Apocalypse countdown, tells you how long it's been since the last apocalypse...",
    "relic counter": "Relic touch counter, tells you how many times you've touched the relic",
    "rank lore": "When players surrender, they gain fanaticism and increase their rank within the order",
    "attack": "",
    "apocalypse": "",
    "faith lore": "",
    "relic": "",
    "relic lore": "",
    "surrender": "Once you've reached this point, the game gets far more nuanced and strategies to gain more fanaticism are frequently talked about. Good luck",
    "end lore": "Once you've beaten the game you will get this lore prompt"}

    return prompt_descriptions

def get_prompt_images():
    prompt_images = {"kotw": "https://media.discordapp.net/attachments/1033211006396137563/1126976706968817704/1.jpg",
    "apoc timer": "https://media.discordapp.net/attachments/1033211006396137563/1126976707329544192/2.jpg",
    "relic counter": "https://media.discordapp.net/attachments/1033211006396137563/1126976707736375419/3.jpg",
    "rank lore": "https://media.discordapp.net/attachments/1033211006396137563/1126976708059344947/4.jpg",
    "attack": "https://media.discordapp.net/attachments/1033211006396137563/1126976708495560856/5.jpg",
    "apocalypse": "https://media.discordapp.net/attachments/1033211006396137563/1126976708894003361/6.jpg",
    "faith lore": "https://media.discordapp.net/attachments/1033211006396137563/1126976709216972970/7.jpg",
    "relic": "https://media.discordapp.net/attachments/1033211006396137563/1126976709556703243/8.jpg",
    "relic lore": "https://media.discordapp.net/attachments/1033211006396137563/1126976709909033102/9.jpg",
    "surrender": "https://media.discordapp.net/attachments/1033211006396137563/1126976710265557083/10.jpg",
    "end lore": "https://media.discordapp.net/attachments/1033211006396137563/1126976726514290789/11.jpg"}

    return prompt_images

class Pkm(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot    

    @app_commands.command(description="Get a link to the progress knight multiplayer wiki")
    async def wiki(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Progress Knight: Multiplayer Wiki", description="The progress knight wiki managed by the community, for the community!\n\nhttps://pk-multiplayer.fandom.com/wiki/", color=0x800080)
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/1116799837707444284/1116800295775768647/pkmulti_icon.png")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(description="Bring up an image of a temple prompt")
    async def temple(self, interaction: discord.Interaction, prompt: str):
        embed = discord.Embed(title="**Temple**", color=0x800080)
        prompt_images = get_prompt_images()
        prompt_descriptions = get_prompt_descriptions()
        
        try:
            embed.set_image(url=prompt_images[prompt])
            embed.description = prompt_descriptions[prompt]
            embed.set_footer(text="All new players should read the temple before asking questions, often your answer can be found here.")
            await interaction.response.send_message(embed=embed)

        except KeyError:
            prompt_names = ""
            for prompt in prompt_descriptions:
                prompt_names += f"\n**{prompt}**"

            embed.description = f"That is not a valid temple prompt, here are some prompts that can be used as references\n{prompt_names}"
            embed.set_footer(text="They are in order, top to bottom based on how early in the story you get them. Do not use the bot to spoil the game for others or you will be punished.")
            await interaction.response.send_message(embed=embed, ephemeral=True)



async def setup(bot: commands.Bot):
    # pkm_discord = bot.get_guild(1108317188999356466)
    # dtd_discord = bot.get_guild(1113670562963791922)
    # whitelisted_guilds = [pkm_discord, dtd_discord]

    print("PKM Loaded")
    await bot.add_cog(Pkm(bot))