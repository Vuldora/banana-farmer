import discord, typing, random
from discord import app_commands
from typing import Literal


async def map_callback(interaction, hom_only: Literal["Yes","No"]):
    maps = ['Bloontonium Mines','Docks','In the Wall','Mayan','Thin Ice','Banana Depot','Basalt Columns','Bloon Bot Factory','Building Site','Castle Ruins','Cobra Command','Dino Graveyard','Garden','Glade','Inflection','Koru','Oasis','Off-tide','Pirate Cove','Ports','Precious Space','Sands of Time','Star','Sun Palace','Salmon Ladder']
    if interaction.data["options"][0]["value"] == "Yes":
        await interaction.response.send_message(maps[random.randint(4,(len(maps) - 1))])
    else:
        await interaction.response.send_message(maps[random.randint(0,(len(maps) - 1))])
map_command = discord.app_commands.Command(
    name="map",
    description="Randomly select a map",
    callback=map_callback,
)
#@app_commands.describe(hom_only="Return only Hall of Masters maps")
#idk if I can just uncomment that or...
