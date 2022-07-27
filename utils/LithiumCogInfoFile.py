from os import PathLike
from typing import Optional, Union, List
import toml

class LithiumCogInfoFile(object):

    name : str
    author : str
    version : Union[str, float]

    description : Optional[str] = ""

    requires : Optional[List[str]] = []
    requires_database : bool = True

    fp : Optional[PathLike] = None # This is added if using the LithiumCogInfoFile.from_file() method

    @classmethod
    def from_file(self, fp : PathLike) -> "LithiumCogInfoFile":

        with open(fp, 'r') as t:
            data = toml.load(t)

        new = LithiumCogInfoFile()

        new.name = data.get('name')
        new.author = data.get('author')
        new.version = data.get('version')

        new.requires = data.get('requires')
        new.requires_database = data.get('requires_database')

        new.description = data.get('description')

        new.fp = fp

        return new

