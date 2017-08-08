import discord, asyncio
from discord.ext import commands
from cogs.utils.checks import *

class massnick:

    def __init__(self, bot):
        self.bot = bot
        self.active = False
        self.guild = None
        self.users = {}

    """
    async def on_member_update(self, before, after):
        if not self.active: return
        if not before.guild == self.guild: return
        if before.nick == after.nick: return
        try:
            await self.bot.change_nickname(before, before.nick)
            print("Someone tried to change his nickname from \"{b}\" to \"{a}\" on guild \"{s}\"!".format(b=before.nick,a=after.nick,s=before.guild.name))
        except discord.Forbidden: print("Insufficient permissions to force \"{n}\" to keep his nickname on guild \"{s}\"".format(n=before.nick,s=before.guild.name))
    """

    @commands.command(aliases=['mn'], pass_context=True)
    async def massnick(self, ctx, onlineonly: bool = False, *, newnick = None):
        """Changes the nickname of all users of the current guild to [newnick]
        Use it a second time to revert all nicknames with a 1 second delay"""
        print('Massnick active on Guild \"%s\" for %s members.'%(self.guild.name, len(self.users)) if self.active else 'Massnick inactive.')
        if not self.active:
            self.guild = ctx.message.guild
            for member in ctx.message.guild.members:
                if onlineonly and member.status == discord.Status.offline: continue
                if member.nick == newnick: continue
                try:
                    _nick = member.nick
                    await member.edit(nick=newnick)
                    self.users[member.id] = _nick
                    print("Saved {n}'s nick as {o}".format(n=member.name,o=member.nick))
                except discord.Forbidden: print("Unable to change {n}'s nick to {o}".format(n=member.name,o=member.nick))
            if len(self.users) == 0: return
            print(self.users)
            self.active = True
        else:
            self.active = False
            for id, oldnick in self.users.items():
                try:
                    if self.guild.get_member(id).nick == oldnick: continue
                except: pass
                try:
                    await self.guild.get_member(id).edit(nick=oldnick)
                    print("Reset {n}'s nick to {o}".format(n=self.guild.get_member(id).name,o=oldnick))
                except discord.Forbidden: print("Unable to reset {n}'s nick to {o}".format(n=self.guild.get_member(id).name,o=oldnick))

    @commands.command(aliases=['rn'], pass_context=True)
    async def resetnicks(self, ctx, *, nick = None):
        """Removes all nicknames on the current guild."""
        for member in ctx.message.guild.members:
            if nick != None and member.nick != nick: continue
            try: await member.edit(nick=None)
            except discord.Forbidden: print("Unable to reset {n}'s nick.".format(n=member.name))

def setup(bot):
    bot.add_cog(massnick(bot))
