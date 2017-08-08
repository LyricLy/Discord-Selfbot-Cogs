import discord, asyncio, datetime
from discord.ext import commands
from cogs.utils.checks import *

class alt:
    """Let's others use u to check their online- and playing status in DM's"""
    active = False
    def __init__(self, bot):
        self.bot = bot

    async def on_message(self, message):
        if not self.active: return
        if not isinstance(message.channel, discord.abc.PrivateChannel): return
        if not message.content.startswith('!'): return
        for guild in self.bot.guilds:
            member = guild.get_member(message.author.id)
            if member: break
        if not member: return await message.channel.send(self.bot.bot_prefix + 'Couldn\'t find you on any of my servers, sorry :( #BlameDiscordAPI')
        if message.content.lower() == "!status":
            await message.channel.send(self.bot.bot_prefix + 'You are currently: `%s`' % member.status)
        elif message.content.lower() in ["!game", "!playing"]:
            if member.game: await message.channel.send(self.bot.bot_prefix + 'You are currently %s: `%s`' % ( "streaming" if member.game.url else "playing", member.game.name+"="+member.game.url if member.game.url else member.game))
            else: await message.channel.send(self.bot.bot_prefix + 'You are currently not playing or streaming anything.')

    @commands.command(aliases=['alt'], pass_context=True)
    async def alttest(self, ctx):
        """Toggles ALT Tester."""
        self.active = not self.active
        await ctx.message.channel.send( self.bot.bot_prefix + 'ALT Tester set to: `%s`' % self.active)

def setup(bot):
    bot.add_cog(alt(bot))
