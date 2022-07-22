from ..ConnectionInfo import ConnectionInfo
from typing import Any

__all__ = [
    "AbstractAdapter"
]

class AbstractAdapter(object):

    identifier : str

    def __init__(self, connection : ConnectionInfo) -> None:
        
        self._connection_info = connection

    async def establish_connection(self) -> Any:
        raise NotImplemented