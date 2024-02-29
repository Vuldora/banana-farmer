import discord, typing, random
from discord import app_commands
from typing import Literal


async def map_callback(interaction, hom_only: Literal["Yes","No"]):
    """Randomly select a map

    Parameters
    -----------
    hom_only: Literal["Yes","No"]
        Return only Hall of Masters maps?
    """
    maps = ['Bloontonium Mines','Docks','In the Wall','Mayan','Thin Ice','Banana Depot','Basalt Columns','Bloon Bot Factory','Building Site','Castle Ruins','Cobra Command','Dino Graveyard','Garden','Glade','Inflection','Koru','Oasis','Off-tide','Pirate Cove','Ports','Precious Space','Sands of Time','Star','Sun Palace','Salmon Ladder']
    if hom_only == "Yes":
        await interaction.response.send_message(maps[random.randint(4,(len(maps) - 1))])
    else:
        await interaction.response.send_message(maps[random.randint(0,(len(maps) - 1))])
        
map_command = discord.app_commands.Command(
    name="map",
    description="Randomly select a map",
    callback=map_callback,
)
