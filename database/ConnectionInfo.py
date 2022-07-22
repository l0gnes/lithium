from dataclasses import dataclass

# NOTE: This more than likely won't hold up for every database out there.

@dataclass
class ConnectionInfo(object):
    host : str
    port : int
    username : str
    password : str
    database : str

    @property
    def as_dict(self) -> dict:
        """Returns all of the connection data as a dictionary.

        :return: A dictionary containing connection information.
        :rtype: dict
        """

        return {
            "host" : self.host,
            "port" : self.port,
            "user" : self.username,
            "password" : self.password,
            "database" : self.database
        }