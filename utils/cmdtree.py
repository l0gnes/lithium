from discord.app_commands import CommandTree
from discord import Interaction

class LithiumCommandTree(CommandTree):

    async def interaction_check(self, interaction: Interaction, /) -> bool:

        # We're only going to check the whitelist if the core is actually hooked
        if interaction.client.db.is_hooked("core"):

            core_hook = interaction.client.db.get_hook("core")
            check = await core_hook.checkForWhitelistedGuild(interaction.guild)
            
            if not check and (interaction.user.id not in self.client.settings.master_user_ids or interaction.guild.id not in self.client.settings.master_guild_ids):

                await interaction.response.send_message(
                    "`⛔` This guild is not whitelisted.\nContact the bot owner if you believe this is a mistake"
                )

                raise core_hook.GuildNotWhitelisted # A little cheeky 

        return await super().interaction_check(interaction)