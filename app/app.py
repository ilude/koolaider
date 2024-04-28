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

activity = discord.CustomActivity(name="Drinking the Good Stuff!")

bot = commands.Bot(command_prefix='!', intents=intents, activity=activity)

def timestamp():
	return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Dictionary to store guild-specific information
guild_store_hash = {}

class GuildInfo:
		def __init__(self, system_channel, channel_id, nix_role):
				self.system_channel = system_channel
				self.channel_id = channel_id
				self.nix_role = nix_role

@bot.event
async def on_ready():
		print(f'{timestamp()}\tLogged in as {bot.user.name}')
		for guild in bot.guilds:
				channel = discord.utils.get(guild.channels, name=CHANNEL_NAME)
				system_channel = guild.system_channel
				role = discord.utils.get(guild.roles, name=ROLE_NAME)

				# Create an instance of GuildInfo for this guild and store it in the guild_info dictionary
				guild_store_hash[guild.id] = GuildInfo(system_channel, channel.id, role)

@bot.event
async def on_message(message):
		guild_store = guild_store_hash.get(message.guild.id)
		if guild_store.nix_role not in message.author.roles and message.channel.id == guild_store.channel_id:
				links = re.findall(URL_PATTERN, message.content)
				print(f'{timestamp()}\t{message.author} posted {len(links)} links to {message.channel}: {message.content}')
				if any(validators.url(link) for link in links):
						await message.author.add_roles(guild_store.nix_role)
						await guild_store.system_channel.send(f'{message.author.mention} is now one of the Kool Kids!')

def signal_handler(signal, frame):
		print(f'{timestamp()}\tStopping the bot...')
		sys.exit(0)

if TOKEN:
		signal.signal(signal.SIGINT, signal_handler)
		signal.signal(signal.SIGTERM, signal_handler)
		bot.run(TOKEN)
else:
		print(f'{timestamp()}\tDiscord bot token not found in the environment variable DISCORD_TOKEN')
