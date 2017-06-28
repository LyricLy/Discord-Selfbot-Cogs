import discord, asyncio
from discord.ext import commands
from cogs.utils.checks import *

class massnick:

    def __init__(self, bot):
        self.bot = bot
        self.active = False
        self.server = 0
        self.users = {}
        config = load_config()
        self.bot_prefix = config["bot_identifier"]
    
    async def on_member_update(self, before, after):
        if not self.active: return
        if not before.server == self.server: return
        if before.nick == after.nick: return
        try:
            await self.bot.change_nickname(before, before.nick)
            print("Someone tried to change his nickname from \"{b}\" to \"{a}\" on server \"{s}\"!".format(b=before.nick,a=after.nick,s=before.server.name))
        except discord.Forbidden: print("Insufficient permissions to force \"{n}\" to keep his nickname on server \"{s}\"".format(n=before.nick,s=before.server.name))

    @commands.command(aliases=['mn'], pass_context=True)
    async def massnick(self, ctx, *, newnick = None):
        if not self.active:
            self.server = ctx.message.server
            for member in ctx.message.server.members:
                self.users[member] = member.nick
                await self.bot.change_nickname(member, newnick)
            print(self.users)
            self.active = True
        else:
            for member, oldnick in self.users:
                await self.bot.change_nickname(member, oldnick)
            self.active = False

def setup(bot):
    bot.add_cog(massnick(bot))
