import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Debugging: Check if the token is loaded
if TOKEN is None:
    raise ValueError("❌ ERROR: Discord Token is missing! Check your .env file.")

# Set bot command prefix
intents = discord.Intents.default()
intents.messages = True  # Ensure the bot can read messages
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot is online! Logged in as {bot.user}")

@bot.command()
async def hello(ctx):
    await ctx.send("👋 Hello! I am your friendly Discord bot.")

# Run the bot
bot.run(TOKEN)
