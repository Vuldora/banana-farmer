import discord, random
from discord import app_commands

towers = ['Dart','Tack','Boomerang','Bomb','Ice','Glue','Sniper','Sub','Boat','Ace','Heli','Mortar','Dartling','Wizard','Super','Ninja','Alchemist','Druid','Village','Farm','Spike Factory','Engineer']

heroes = ['Quincy','Cyber Quincy','Gwen','Science Gwen','Obyn','Ocean Obyn','Striker Jones','Biker Bones','Churchill','Sentai','Benjamin','DJ Benjammin','Ezili','Smudge Catt Ezili','Pat Fusty','Snowpat','Jericho','Highwayman','Star Captain','Adora']

async def quad_callback(interaction):
    quad = random.sample(towers, k=3)
    await interaction.response.send_message(quad[0] + ", " + quad[1] + ", " + quad[2] + ", and " + heroes[random.randint(0,(len(heroes) - 1))])

quad_command = discord.app_commands.Command(
    name="quad",
    description="Randomly generate a tower loadout",
    callback=quad_callback
)

