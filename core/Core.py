import discord
from discord import app_commands
from discord.ext import commands
from .db.hook import CoreDatabaseHook
from typing import List
from utils.LithiumCog import LithiumCog
from utils.LithiumCogInfoFile import LithiumCogInfoFile
from .utils import repoutils

class Core(LithiumCog):

    db_hook : CoreDatabaseHook # While redundant, it helps for linting
    db_hook_class = CoreDatabaseHook # This is the one that actually matters

    ### This should only ever be done in the core cog

    cog_id = "core"
    name = "Core"
    author = "l0gnes"
    version = 1.0

    requires_database = True

    ###

    whitelist_commands = app_commands.Group(
        name = "whitelist",
        description = "Administrative commands to whitelist guilds for the bot"
    )

    repo_commands = app_commands.Group(
        name = "repo",
        description = "The gateway command to community cogs"
    )

    def __init__(self, client : commands.Bot):
        self.client = client

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


    @repo_commands.command(name = "add", description = "Adds a repository to the repository list")
    async def core_repo_add(self, interaction : discord.Interaction, url : str):
        
        repoutils.ensure_repos_directory_exists()

        x = repoutils.decipher_github_uri(url)

        if not x:
            return await interaction.response.send_message(
                "Link must be a valid github url."
            )

        repo_info = await repoutils.fetch_github_repo_info(*x)

        if not repo_info:
            return await interaction.response.send_message(
                "Failed to find that repository."
            )

        # await interaction.response.send_message(
        #     "Hello World!",
        #     embed = discord.Embed(
        #         title = repo_info['full_name']
        #     ).set_author(
        #         name = repo_info['owner']['login'],
        #         icon_url = repo_info['owner']['avatar_url']
        #     )
        # )

        # TODO: Insert extra verification steps here with like a button or something idk

        repoutils.create_github_user_folder(repo_info['owner']['login'])

        repo_dir = "./repos/%s/%s" % (repo_info['owner']['login'], repo_info['name'])

        repoutils.clone_repository(
            repo_info['clone_url'],
            repo_dir
        )

        valid_toml_files = repoutils.check_for_valid_cog_tomls(repo_dir)
        cog_info_object_array = [ LithiumCogInfoFile.from_file(i) for i in valid_toml_files ]

        await interaction.response.send_message(
            f"{len(cog_info_object_array)} new cogs are available: " + ", ".join(
                map(lambda n: n.name, cog_info_object_array
            ))
        )







