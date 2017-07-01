import discord, asyncio
from discord.ext import commands
from cogs.utils.checks import *

class massnick:

    def __init__(self, bot):
        self.bot = bot
        self.active = False
        self.server = None
        self.users = {}
        config = load_config()
        self.bot_prefix = config["bot_identifier"]
    
    """
    async def on_member_update(self, before, after):
        if not self.active: return
        if not before.server == self.server: return
        if before.nick == after.nick: return
        try:
            await self.bot.change_nickname(before, before.nick)
            print("Someone tried to change his nickname from \"{b}\" to \"{a}\" on server \"{s}\"!".format(b=before.nick,a=after.nick,s=before.server.name))
        except discord.Forbidden: print("Insufficient permissions to force \"{n}\" to keep his nickname on server \"{s}\"".format(n=before.nick,s=before.server.name))
    """

    @commands.command(aliases=['mn'], pass_context=True)
    async def massnick(self, ctx, *, newnick = None):
        """Changes the nickname of all users of the current server to [newnick]
        Use it a second time to revert all nicknames with a 1 second delay"""
        if not self.active:
            self.server = ctx.message.server
            for member in ctx.message.server.members:
                try:
                    await self.bot.change_nickname(member, newnick)
                    self.users[member.id] = member.nick
                    print("Saved {n}'s nick as {o}".format(n=member.name,o=member.nick))
                except discord.Forbidden: print("Unable to change {n}'s nick to {o}".format(n=member.name,o=member.nick))
            print(self.users)
            self.active = True
        else:
            self.active = False
            for id, oldnick in self.users.items():
                try:
                    await self.bot.change_nickname(self.server.get_member(id), oldnick)
                    print("Reset {n}'s nick to {o}".format(n=self.server.get_member(id).name,o=oldnick))
                    await asyncio.sleep(1)
                except discord.Forbidden: print("Unable to reset {n}'s nick to {o}".format(n=self.server.get_member(id).name,o=oldnick))

    @commands.command(aliases=['rn'], pass_context=True)
    async def resetnicks(self, ctx, *, nick = None):
        """Removes all nicknames on the current server."""
        for member in ctx.message.server.members:
            if nick != None and member.nick != nick: continue
            await self.bot.change_nickname(member, None)

def setup(bot):
    bot.add_cog(massnick(bot))
