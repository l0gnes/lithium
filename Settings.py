import toml
from typing import List
from os import PathLike

class SettingsObject(object):

    bot_token           : str

    db_adapter          : str       = "asyncpg"
    db_address          : str       = "0.0.0.0"
    db_port             : int       = 5432
    db_username         : str
    db_password         : str
    db_database         : str       = "lithium"

    dump_empty_env      : bool      = False
    public_instance     : bool      = False

    master_user_ids     : List[int] = []
    master_guild_ids    : List[int] = []

    activity_enabled    : bool      = True
    activity_name       : str       = "Lithium 🧋"
    activity_type       : str       = "PLAYING"
    activity_livestream_link : str  = "https://twitch.tv/wendys"

    @classmethod
    def load_from_file(cls, fp : PathLike) -> "SettingsObject":
        """Returns a settings object from a file's contents.

        :param fp: The path to the file
        :type fp: PathLike
        :return: The settings file containing the settings from said file
        :rtype: SettingsObject
        """

        with open(fp, "r", encoding="utf-8") as tml:
            data = toml.load(tml)

        newObj = cls()

        newObj.bot_token = data['STARTUP']['TOKEN']

        newObj.db_adapter = data["DATABASE"]["ADAPTER"]
        newObj.db_address = data["DATABASE"]["ADDRESS"]
        newObj.db_port = data["DATABASE"]["PORT"]
        newObj.db_username = data["DATABASE"]["USERNAME"]
        newObj.db_password = data["DATABASE"]["PASSWORD"]

        newObj.dump_empty_env = data["SETTINGS"]["DUMP_EMPTY_ENVIRONMENT"]
        newObj.public_instance = data["SETTINGS"]["PUBLIC_BOT_INSTANCE"]

        newObj.master_user_ids = data["SETTINGS"]["MASTER_USER_IDS"]
        newObj.master_guild_ids = data["SETTINGS"]["MASTER_GUILD_IDS"]

        newObj.activity_enabled = data["ACTIVITY"]["ENABLED"]
        newObj.activity_name = data["ACTIVITY"]["NAME"]
        newObj.activity_type = data["ACTIVITY"]["TYPE"]
        newObj.activity_livestream_link = data["ACTIVITY"]["LIVESTREAM_LINK"]

        return newObj