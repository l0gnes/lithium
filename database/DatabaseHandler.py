"""

    As of right now this only supports PostgreSQL.

"""

import asyncio
import asyncpg
from .adapters import AbstractAdapter
from .ConnectionInfo import ConnectionInfo
from typing import Type, Union
from .DatabaseHook import DatabaseHook
from .errors import DatabaseHookKeyAlreadyAssigned, UnsupportedAdapter
from asyncio import AbstractEventLoop, get_event_loop

__all__ = [
    "DatabaseHandler"
]

class DatabaseHandler(object):

    def __init__(self, event_loop : AbstractEventLoop, connection : ConnectionInfo, adapter : Type[AbstractAdapter]) -> None:

        self._connection_info = connection
        self._adapter = adapter(self._connection_info)
        self.loop = event_loop

        self.pool = None

        self.hooks = {}

    async def attempt_connection(self) -> None:
        """
            Attempts to resolve a connection to the database and assigns the pool attribute if it can.
        """
        # TODO: Better error logging and implement a better way of assigning the pool as some databases may not support connection pooling
        try:
            self.pool = await self._adapter.establish_connection()

        except Exception as err:
            raise err

    def get_hook(self, key : str) -> Union[DatabaseHook, None]:
        """A more functional approach than directly grabbing the hook from the database

        :param key: The identifier for the hook
        :type key: str
        :return: The database hook if it can be found, otherwise, None
        :rtype: Union[DatabaseHook, None]
        """
        return self.hooks.get(key, None)

    async def set_hook(self, key : str, hook : DatabaseHook) -> None:
        """Assigns the hook a place in the hooks array so that it can be used throughout the bot

        :param key: The key to assign the hook to
        :type key: str
        :param hook: The hook to add to the hook reference
        :type hook: DatabaseHook
        """
        
        if self.get_hook(key = key):
            raise DatabaseHookKeyAlreadyAssigned

        if self.adapter_identifier not in hook.supported_adapters:
            raise UnsupportedAdapter

        initialized_hook = hook(db = self)
        await initialized_hook.initialHookQuery()

        self.hooks[key] = initialized_hook

    def is_hooked(self, key : str) -> bool:
        """Returns whether or not a hook exists in the reference

        :param key: The reference key for the hook
        :type key: str
        :return: True if hook exists, False otherwise
        :rtype: bool
        """
        return key in self.hooks.keys()

    @property
    def adapter_type(self) -> Type:
        """Returns the type of the database adapter

        :return: The type of the database adapter
        :rtype: Type
        """
        return type(self._adapter)

    @property
    def adapter_identifier(self) -> str:
        """Returns the string-based identifier for the database adapter

        :return: The identifier for the database adapter
        :rtype: str
        """
        return self._adapter.identifier
