from . import LithiumCog
import toml
from os.path import dirname, exists
from os import PathLike

class LithiumCommunityCog(LithiumCog):

    custom_toml_filepath : PathLike = None

    def load_data_from_cog_toml(self, *, fp : PathLike = None):

        if not fp:
            dest = dirname(__file__ + "/cog.toml")

        else:
            dest = fp

        if not exists(dest):
            raise FileNotFoundError("Failed to locate the cog.toml file for this cog.")

        d = toml.load(dest)

        self.requires = d.get('requires', [])
        self.requres_database = d.get('requires_database', True)

        self.cog_id = d.get("cog_id", '')

        self.name = d.get('name', 'Unnamed Community Cog')
        self.author = d.get("author", "Unknown")
        self.version = d.get("version", 0)

        self.description = d.get("description", "No description provided.")

    async def cog_load(self):

        self.load_data_from_cog_toml(
            fp = self.custom_toml_filepath
        )

        return await super().cog_load()
