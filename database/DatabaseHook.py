from typing import Tuple

class DatabaseHook(object):
    """
        Hooks into the database to provide more functionality.
        This probably isn't a good way of coding, but it's python
        so I can be as dynamic as I want wherever I want 😈
    """

    def __init__(self, db : "DatabaseHandler") -> None:
        self.db = db

    # A list of the supported adapters for this hook
    supported_adapters : Tuple[str] = ()

    async def initialHookQuery(self) -> None:
        return