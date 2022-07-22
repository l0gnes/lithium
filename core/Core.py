import discord
from discord import app_commands
from discord.ext import commands
from .db.hook import CoreDatabaseHook

class Core(commands.Cog):

    def __init__(self, client : commands.Bot):
        self.client = client

    async def cog_load(self):
        try:
            await self.client.db.set_hook(
                "core", CoreDatabaseHook
            )
        except Exception as err:
            raise err
        else:
            self.db_hook = self.client.db.get_hook("core")

    @app_commands.command(name="ping", description="Check to see if the bot is up!")
    async def core_ping(self, interaction : discord.Interaction) -> None:
        await interaction.response.send_message(
            "`🧋` Pong! `%sms`" % ( round(self.client.latency * 1000 , 2) ),
            ephemeral = True
        )