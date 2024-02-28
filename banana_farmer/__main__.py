import discord, random, banana_farmer
from discord import app_commands
from banana_farmer import DISCORD_TOKEN
from banana_farmer.commands import map, quad, player, leaderboard

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    # doing this manually sucks there is probably a way to automate it
    tree.add_command(map.map_command)
    tree.add_command(quad.quad_command)
    tree.add_command(player.player_command)
    tree.add_command(leaderboard.leaderboard_command)
    # -------------------------------------------------
    await tree.sync() 
    cute_people = ['Emilplane','Ryan Mehalic','Cologne', 'Paytrolah']
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=cute_people[random.randint(0,len(cute_people)-1)]))
    print("Initilization Complete")

client.run(DISCORD_TOKEN)
