import os
import discord
import random
import time
from discord import app_commands

intents = discord.Intents.default()
intents.message_content = True

class CatBot(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

bot = CatBot()

MEOWS = [
    "meow",
    "mrrp",
    "meooow",
    "miau"
]

last_meow = {}
COOLDOWN = 60  # seconds

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    now = time.time()
    channel_id = message.channel.id

    if channel_id in last_meow and now - last_meow[channel_id] < COOLDOWN:
        return

    if random.randint(1, 25) == 1:
        last_meow[channel_id] = now
        await message.channel.send(random.choice(MEOWS))

# 🔧 TEST COMMAND
@bot.tree.command(name="meow", description="Make ABX’s cat meow")
async def meow_command(interaction: discord.Interaction):
    await interaction.response.send_message(random.choice(MEOWS))

bot.run(os.getenv("TOKEN"))
