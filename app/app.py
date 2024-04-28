from datetime import datetime
import os
import signal
import sys
import re
import discord
from discord.ext import commands
import validators

# Get the bot token from the environment variable
TOKEN = os.environ.get('DISCORD_TOKEN')

# Replace with the channel name of the "koolaid-links" channel
CHANNEL_NAME = 'koolaid-links'

# Replace with the name of the "system-messages" channel
SYSTEM_CHANNEL_NAME = 'system-messages'

# Replace with the role name of the "Nix User" role
ROLE_NAME = 'Nix User'

# List of common image file extensions
IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']

# Regular expression pattern to match non-image URLs
URL_PATTERN = r'https?://\S+?(?!(?:' + '|'.join(re.escape(ext) for ext in IMAGE_EXTENSIONS) + r'))\S*'

intents = discord.Intents.default()
intents.message_content = True
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix='!', intents=intents, activity=discord.Game(name="Drinking the Good Stuff!"))

@bot.event
async def on_ready():
		print(f'Logged in as {bot.user.name}')
		for guild in bot.guilds:
				channel = discord.utils.get(guild.channels, name=CHANNEL_NAME)
				if channel:
						global CHANNEL_ID
						CHANNEL_ID = channel.id

				system_channel = discord.utils.get(guild.channels, name=SYSTEM_CHANNEL_NAME)
				if system_channel:
						global SYSTEM_CHANNEL_ID
						SYSTEM_CHANNEL_ID = system_channel.id

				role = discord.utils.get(guild.roles, name=ROLE_NAME)
				if role:
						global NIX_ROLE
						NIX_ROLE = role
				break


validate_url = lambda link: validators.url(link)

@bot.event
async def on_message(message):
		if NIX_ROLE not in message.author.roles and message.channel.id == CHANNEL_ID:
				links = re.findall(URL_PATTERN, message.content)
				print(f'{ datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\t{message.author} posted {len(links)} links to {message.channel}: {message.content}')
				if any(validate_url(link) for link in links):
						await message.author.add_roles(NIX_ROLE)
						system_channel = bot.get_channel(SYSTEM_CHANNEL_ID)
						await system_channel.send(f'{message.author.mention} is now one of the Kool Kids!')

def signal_handler(signal, frame):
		print('Stopping the bot...')
		sys.exit(0)

if TOKEN:
		signal.signal(signal.SIGINT, signal_handler)
		signal.signal(signal.SIGTERM, signal_handler)
		bot.run(TOKEN)
else:
		print('Discord bot token not found in the environment variable DISCORD_TOKEN')