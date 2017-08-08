import discord, asyncio
from discord.ext import commands
from cogs.utils.checks import *

class nickprotect:

    def __init__(self, bot):
        self.bot = bot
        self.active = True
        self.allowed = False

    async def on_member_update(self, before, after):
        if not self.active: return
        if not before == self.bot.user: return
        if before.nick == after.nick: return
        if self.allowed: self.allowed = False; return
        if after.guild.me.guild_permissions.change_nickname:
            self.allowed = True
            await before.edit(nick=before.nick)
            print("Someone tried to change my nickname from \"{b}\" to \"{a}\" on guild \"{s}\"!".format(b=before.nick,a=after.nick,s=before.guild.name))
            # msg = await self.bot.send_message(before.guild., 'Please don\'t try to change my nickname but ask me to change it instead')
            # await asyncio.sleep(5)
            # await self.bot.delete_message(msg)
        else: return print("Insufficient permissions to protect own nickname \"{n}\" on guild \"{s}\"".format(n=before.nick,s=before.guild.name))

    @commands.command(aliases=['np'], pass_context=True)
    async def nickprotect(self, ctx):
        """Toggles nickprotect mode so you keep your nick when you have enough permissions."""
        await ctx.message.delete()
        self.active = not self.active
        await ctx.message.channel.send( self.bot.bot_prefix + 'Nickprotect set to: `%s`' % self.active)

def setup(bot):
    bot.add_cog(nickprotect(bot))
