from typing import Any, List
from database import DatabaseHook, DatabaseHandler
from discord import Guild, User
import os.path

__all__ = [
    "CoreDatabaseHook"
]

class CoreDatabaseHook(DatabaseHook):

    supported_adapters = (
        "asyncpg",
    )

    def __init__(self, db : DatabaseHandler) -> None:
        self.db = db

    async def initialHookQuery(self) -> None:

        file_dir = os.path.dirname(__file__)
        schema_path = "%s\\schema.sql" % file_dir

        with open(schema_path, "r", encoding="utf-8") as schema_file:
            schema_contents = schema_file.read()

        async with self.db.pool.acquire() as connection:

            async with connection.transaction():

                await connection.execute(schema_contents)

    async def addWhitelistedGuild(self, executor : User, guild : Guild) -> None:

        async with self.db.pool.acquire() as connection:
            
            async with connection.transaction():

                await connection.execute(
                    "INSERT INTO guild_whitelist VALUES ($1, $2, CURRENT_TIMESTAMP);", 
                    guild.id, executor.id
                )

    async def fetchWhitelistedGuildIds(self) -> List[int]:
        
        async with self.db.pool.acquire() as connection:

            async with connection.transaction():

                result = await connection.fetch("SELECT guildid FROM guild_whitelist;")
        
        return result

    async def checkForWhitelistedGuild(self, guild : Guild) -> bool:

        async with self.db.pool.acquire() as connection:

            async with connection.transaction():

                result = await connection.fetchrow("SELECT guildid FROM guild_whitelist WHERE guildid=$1", guild.id)

        return result is not None