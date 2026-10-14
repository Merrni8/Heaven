import discord
from discord.ext import commands
from discord import app_commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="clear", description="Usuń wiadomości")
    @app_commands.describe(amount="Ile wiadomości usunąć (max 100)")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def clear(self, interaction: discord.Interaction, amount: int):
        if amount < 1 or amount > 100:
            await interaction.response.send_message("Podaj liczbę od 1 do 100.", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)
        deleted = await interaction.channel.purge(limit=amount)
        await interaction.followup.send(f"Usunięto {len(deleted)} wiadomości.", ephemeral=True)

    @app_commands.command(name="kick", description="Wyrzuć kogoś z serwera")
    @app_commands.describe(member="Kogo wyrzucić", reason="Powód")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = "Brak powodu"):
        if member.top_role >= interaction.user.top_role:
            await interaction.response.send_message("Nie możesz wyrzucić kogoś z równą lub wyższą rolą.", ephemeral=True)
            return

        await member.kick(reason=reason)
        await interaction.response.send_message(f"Wyrzucono {member.mention}. Powód: {reason}")

    @app_commands.command(name="ban", description="Zbanuj kogoś")
    @app_commands.describe(member="Kogo zbanować", reason="Powód")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = "Brak powodu"):
        if member.top_role >= interaction.user.top_role:
            await interaction.response.send_message("Nie możesz zbanować kogoś z równą lub wyższą rolą.", ephemeral=True)
            return

        await member.ban(reason=reason)
        await interaction.response.send_message(f"Zbanowano {member.mention}. Powód: {reason}")

    @clear.error
    @kick.error
    @ban.error
    async def mod_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message("Nie masz uprawnień do tej komendy.", ephemeral=True)
        else:
            await interaction.response.send_message("Wystąpił błąd.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Moderation(bot))
