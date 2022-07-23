import discord
from discord import app_commands
from discord.ext import commands
from .db.hook import CoreDatabaseHook
from typing import List

class Core(commands.Cog):

    db_hook : CoreDatabaseHook

    whitelist_commands = app_commands.Group(
        name = "whitelist",
        description = "Administrative commands to whitelist guilds for the bot"
    )

    def __init__(self, client : commands.Bot):
        self.client = client

    async def cog_load(self):
        try:
            await self.client.db.set_hook(
                "core", CoreDatabaseHook
            )
        except Exception as err:
            raise err
        else:
            self.db_hook = self.client.db.get_hook("core")

    @app_commands.command(name="ping", description="Check to see if the bot is up!")
    async def core_ping(self, interaction : discord.Interaction) -> None:
        await interaction.response.send_message(
            "`🧋` Pong! `%sms`" % ( round(self.client.latency * 1000 , 2) ),
            ephemeral = True
        )

    @commands.is_owner() # TODO: Add a proper check that checks for master users rather than the bot owner
    @whitelist_commands.command(name="add", description="Add a guild to the bot's whitelist.")
    async def core_whitelist_add(self, interaction : discord.Interaction, guild : str):

        try:

            ctx = await commands.Context.from_interaction(interaction)
            converted_guild = await commands.GuildConverter().convert(
                ctx,
                guild
            )

        except commands.ConversionError:

            return await interaction.response.send_message(
                "The argument provided was not a valid guild!",
                ephemeral = True,
            )

        else:

            check = await self.db_hook.checkForWhitelistedGuild(guild=converted_guild)

            if not check:

                await self.db_hook.addWhitelistedGuild(executor=interaction.user, guild=converted_guild)

                return await interaction.response.send_message(
                    "`%s` has been added to the bot's whitelist!" % (converted_guild.name)
                )

            else:

                return await interaction.response.send_message(
                    "Failed to whitelist the guild: `%s`, it is already whitelisted!" % (converted_guild.name)
                )

    @commands.is_owner()
    @whitelist_commands.command(name="remove", description="Remove a guild from the bot's whitelist.")
    async def core_whitelist_remove(self, interaction : discord.Interaction, guild : str):

        try:

            ctx = await commands.Context.from_interaction(interaction)
            converted_guild = await commands.GuildConverter().convert(
                ctx, guild
            )

        except commands.ConversionError:

            return await interaction.response.send_message(
                "The argument provided was not a valid guild."
            )

        else:

            check = await self.db_hook.checkForWhitelistedGuild(converted_guild)

            if not check:

                return await interaction.response.send_message(
                    "Failed to locate the guild `%s` in the whitelist." % (converted_guild.name)
                )

            else:

                await self.db_hook.removeWhitelistedGuild(converted_guild)

                return await interaction.response.send_message(
                    "`%s` has been removed from the whitelist." % (converted_guild.name)
                )

    @commands.is_owner()
    @whitelist_commands.command(name="list", description="Provides a list of all the whitelisted guilds on the bot")
    async def core_whitelist_list(self, interaction : discord.Interaction):

        guild_ids = await self.db_hook.fetchWhitelistedGuildIds()

        

        # This method excludes guilds that the bot isn't a part of anymore
        # which should make for a cleaner pagination
        guilds = list(
            filter(
                lambda g: g.id in map(lambda o: o['guildid'], guild_ids),
                self.client.guilds
            )
        )

        paginator = commands.Paginator()
        
        paginator.add_line(
            "Showing %s whitelisted guilds:" % (len(guilds))
        )

        for g in guilds:
            paginator.add_line("  \u2B9A " + g.name)

        # ! Technically I don't know if you can respond to an interaction twice, but we'll cross this path when we get to it

        for page in paginator.pages:
            await interaction.response.send_message(page)


