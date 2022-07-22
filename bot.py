import discord
from discord.ext import commands
from discord.app_commands import CommandTree
from database import DatabaseHandler, ConnectionInfo
from database.adapters import PostgresSQLAdapter
from Settings import SettingsObject
import os.path

__all__ = [
    "Lithium"
]

class Lithium(commands.Bot):

    db : DatabaseHandler
    settings : SettingsObject

    def __init__(self, *args, **kwargs) -> None:

        self.settings = self.load_settings()
        
        activity = None
        if self.settings.activity_enabled:
            activity = discord.Activity(
                name = self.settings.activity_name,
                url = self.settings.activity_livestream_link,
                type = {
                    "PLAYING" : discord.ActivityType.playing,
                    "LISTENING" : discord.ActivityType.listening,
                    "WATCHING" : discord.ActivityType.watching,
                    "STREAMING" : discord.ActivityType.streaming,
                    "COMPETING" : discord.ActivityType.competing,
                }[self.settings.activity_type]
            )

        super().__init__(
            command_prefix = ".",
            help_command = None,
            intents = discord.Intents.all(),
            application_id = 878908931534106635,
            activity = activity
        )

        self.db = DatabaseHandler(
            event_loop = self.loop,
            connection = ConnectionInfo(
                host = self.settings.db_address,
                port = self.settings.db_port,
                username = self.settings.db_username,
                password = self.settings.db_password,
                database = self.settings.db_database
            ),
            adapter = PostgresSQLAdapter
        )

    def load_settings(self) -> None:
        if os.path.exists("./env.toml"):
            
            return SettingsObject.load_from_file(
                "./env.toml"
            )

        elif os.path.exists("./env.example.toml"):

            with open("./env.example.toml", "r", encoding="utf-8") as template_env:
                tmp = template_env.read()

            with open("./env.toml", "w+", encoding="utf-8") as new_env:
                new_env.write(tmp)

            # TODO: Add proper logging 
            print("Please edit the newly created env.toml with your bot settings.")

            quit() 

        else:
            
            # TODO: Create a proper exception for this
            # This is raised when the bot can't find the env.example.toml file and no env.toml exists
            # NOTE: We could possibly pull the toml file directly from github and remove this error entirely?
            raise Exception
            

    async def setup_cogs(self) -> None:

        try:
            await self.load_extension("core")
        except Exception as err:
            raise err    

    async def setup_hook(self) -> None:

        for guild_id in self.settings.master_guild_ids:
            
            obj = discord.Object(id=guild_id)
            self.tree.copy_global_to(guild=obj)

        await self.tree.sync()

        return await super().setup_hook()

    async def bot_start_function(self) -> None:

        await self.db.attempt_connection()
        await self.setup_cogs()

        await self.start(token = self.settings.bot_token)

if __name__ == "__main__":
    print(__file__) 