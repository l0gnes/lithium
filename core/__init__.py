from . import Core
from discord.ext.commands import Bot

async def setup(client : Bot):
    await client.add_cog(
        Core.Core(
            client = client
        )
    )