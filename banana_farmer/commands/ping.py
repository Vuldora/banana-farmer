import discord
from discord import app_commands

async def ping_callback(interaction):
    await interaction.response.send_message("Pong! " + str(client.latency*1000) + "ms")
ping_command = discord.app_commands.Command(
    name="ping",
    description="ping the bot",
    callback =  ping_callback,
)


