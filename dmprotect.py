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
        if not message.channel.type == discord.ChannelType.private: return
        if self.allowed: self.allowed = False; return
        print('+')
        print('message.channel.created_at: %s'%message.channel.created_at)
        print('message.timestamp: %s'%message.timestamp)
        print('datetime.datetime.now(): %s'%datetime.datetime.now())
        print('%s'%message.channel.created_at == message.timestamp)
        print('-')
        # logs = yield from self.bot.logs_from(message.channel, limit=1)
        # print('length: %s'%len(logs))
        if any(s in message.content for s in self.invites):
            block_user(message.author.id)

    @commands.command(aliases=['dmp'], pass_context=True)
    async def dmprotect(self, ctx):
        """Toggles DM Invite Protection."""
        self.active = not self.active
        self.allowed = True
        await self.bot.send_message(ctx.message.channel, self.bot.bot_prefix + 'DM Protection set to: `%s`' % self.active)

def setup(bot):
    bot.add_cog(dmprotect(bot))
