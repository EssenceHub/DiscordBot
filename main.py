import discord
from discord.ext import commands
from os import getenv
from dotenv import load_dotenv
from Factory.utils import reload_response_buttons

# Config
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="$", intents=intents, help_command=None)
load_dotenv()

@bot.command(name="sync")  # Sync Command for testing
@commands.is_owner()
async def sync(ctx: commands.Context):
    async with ctx.typing():
        await bot.tree.sync()
        await ctx.send("Synchronized!")

# Cogs
async def load_extensions():
    await bot.load_extension('Cogs.settings')
    await bot.load_extension('Cogs.moderation')
    await bot.load_extension('Cogs.logs')
    await bot.load_extension('Cogs.user')
    await bot.load_extension('Cogs.party')
    await bot.load_extension('Cogs.arcane')
    await bot.load_extension('Cogs.idle')
    await bot.load_extension('Cogs.pkm')

# Bot events
@bot.event
async def on_ready():
    await load_extensions()
    await reload_response_buttons(bot)
    print("Bot Online")

# Token
token = getenv("ESSENCE")
bot.run(token)