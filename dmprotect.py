import discord, asyncio, datetime
from discord.ext import commands
from cogs.utils.checks import *
from cogs.utils.api import block_user

class dmprotect:
    active = False
    allowed = False
    invites = ['discord.gg', 'discord.io', 'discordapp.com/invite']
    def __init__(self, bot):
        self.bot = bot

    async def on_message(self, message):
        if not self.active: return
        if not isinstance(message.channel, discord.abc.PrivateChannel): return
        if self.allowed: self.allowed = False; return
        messages = await message.channel.history(limit=2).flatten()
        if not len(messages) == 1: return print('not first message')
        for invite in self.invites:
            if invite in message.content:
                block_user(message.author.id)
                print('User %s#%s used \"%s\" in first private message, therefor i blocked him for you!'%(message.author.name, message.author.discriminator, invite))
                return

    @commands.command(aliases=['dmp'], pass_context=True)
    async def dmprotect(self, ctx):
        """Toggles DM Invite Protection."""
        await ctx.message.delete()
        self.active = not self.active
        self.allowed = True
        await ctx.message.channel.send( self.bot.bot_prefix + 'DM Protection set to: `%s`' % self.active)

def setup(bot):
    bot.add_cog(dmprotect(bot))
