from discord.ext import commands
from typing import List, Optional, Type, Union
from database import DatabaseHook

class LithiumCog(commands.Cog):

    requires : List[str] = []
    requires_database : bool = True

    db_hook : Optional[DatabaseHook] = None
    db_hook_class : Optional[Type[DatabaseHook]] = None
    cog_id: str # This must be unique amongst all of the LithiumCogs, this is also used for db hook keys
    
    name : Optional[str]
    author : Optional[str]
    version : Optional[Union[str, float]]

    description : Optional[str] = ""
    
    async def cog_load(self):

        if self.requires_database and self.db_hook_class is not None:

            try:
                await self.client.db.set_hook(
                    self.cog_id, self.db_hook_class
                )
            except Exception as err:
                raise err
            else:
                self.db_hook_class = self.client.db.get_hook(self.cog_id)

        print(f"Cog: {self.name} {self.version} by {self.author} has been loaded")

        return await super().cog_load()

    async def lithium_cog_after_load(self):
        # Checks to make sure that everything that is required to be loaded actually is
        # We do this after because I'm too lazy to do checking before loading the cogs.
        # This is probably bad since you shouldn't have to unload a cog that shouldn't
        # have been loaded in the first place but oh well lmao

        # TODO: Check to make sure that "requires" has it's requirements met.
        return False