import discord, os, pathlib
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

BASE_DIR = pathlib.Path(__file__).parent
COMMANDS_DIR = BASE_DIR / "commands" 
