import discord
from discord.ext import commands
import config

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(config.WELCOME_CHANNEL_ID)
        if channel is None:
            return

        embed = discord.Embed(
            title="Witaj na serwerze Heaven!",
            description=f"Cześć {member.mention}!\nMiło Cię widzieć ❤️",
            color=discord.Color.pink()
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text=f"Jesteś {len(member.guild.members)}. osobą na serwerze")
        
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.bot.get_channel(config.GOODBYE_CHANNEL_ID)
        if channel is None:
            return

        embed = discord.Embed(
            title="Żegnaj...",
            description=f"{member.name} opuścił serwer.",
            color=discord.Color.dark_grey()
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        
        await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Welcome(bot))
