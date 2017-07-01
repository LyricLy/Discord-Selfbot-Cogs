import discord, asyncio
from discord.ext import commands
from cogs.utils.checks import *

class nickprotect:

    def __init__(self, bot):
        self.bot = bot
        self.active = True
        self.allowed = False
        config = load_config()
        self.bot_prefix = config["bot_identifier"]
    
    async def on_member_update(self, before, after):
        if not self.active: return
        if not before == self.bot.user: return
        if before.nick == after.nick: return
        if self.allowed: self.allowed = False; return
        try:
        # if before.nick == None: before.nick = ""
            self.allowed = True
            await self.bot.change_nickname(before, before.nick)
            print("Someone tried to change my nickname from \"{b}\" to \"{a}\" on server \"{s}\"!".format(b=before.nick,a=after.nick,s=before.server.name))
        # msg = await self.bot.send_message(before.server., 'Please don\'t try to change my nickname but ask me to change it instead')
        # await asyncio.sleep(5)
        # await self.bot.delete_message(msg)
        except discord.Forbidden: print("Insufficient to protect own nickname \"{n}\" on server \"{s}\"".format(n=before.nick,s=before.server.name))

    @commands.command(aliases=['np'], pass_context=True)
    async def nickprotect(self, ctx):
        """Toggles nickprotect mode so you keep your nick when you have enough permissions."""
        self.active = not self.active
        await self.bot.send_message(ctx.message.channel, self.bot.bot_prefix + 'Nickprotect set to: `%s`' % self.active)

def setup(bot):
    bot.add_cog(nickprotect(bot))
