import discord, asyncio, requests, os
from discord.ext import commands
from cogs.utils.checks import *
from cogs.utils.api import *

class UserInteractionRequiredException(Exception): pass

# noinspection PyStatementEffect,PyUnreachableCode
class globalban:

    def __init__(self, bot):
        self.bot = bot
        raise UserInteractionRequiredException('\nATTENTION: This cog may contain bugs and is only intended to be used by advanced users.\nRemove line 13 from cogs/globalban.py to use this cog!')

    def get_user(self, user, message):
        try:
            member = get_user(message,user)
            if member: return member
            for server in self.bot.servers:
                member = server.get_member(int(user))
                if member: return member

            """client = discord.Client()

            @client.event
            async def on_ready():
              print('Logged in as')
              print(client.user.name)
              print(client.user.id)
              print('------')

            client.run('***REMOVED***')
            return client.get_user_info(int(user))"""
            return False
        except:
            pass


    @commands.command(aliases=['fu'], pass_context=True)
    async def finduser(self, ctx, *, user):
        """Debug command. Checks if we could find the user you're searching for."""
        try:
            member = self.get_user(user,ctx.message)
            if not member: await self.bot.send_message(ctx.message.channel, "User \"%s\" not found."%user); return
            await self.bot.send_message(ctx.message.channel, "User found: %s" % member.name)
        except:
            from traceback import format_exc;await self.bot.send_message(ctx.message.channel, self.bot.bot_prefix + " Error:\n\n%s" % format_exc())

    @commands.command(aliases=['bl'], pass_context=True)
    async def block(self, ctx, *, user):
        """Blocks the user you provide."""
        try:
            member = self.get_user(user,ctx.message)
            block_user(member.id)
            await self.bot.send_message(ctx.message.channel, 'Blocked user %s'%user)
        except:
            from traceback import format_exc;await self.bot.send_message(ctx.message.channel, self.bot.bot_prefix + " Error:\n\n%s" % format_exc())

    @commands.command(aliases=['ubl'], pass_context=True)
    async def unblock(self, ctx, *, user):
        """Unblocks the user you provide."""
        try:
            member = self.get_user(user,ctx.message)
            unblock_user(member.id)
            await self.bot.send_message(ctx.message.channel, 'Unblocked user %s'%user)
        except:
            from traceback import format_exc;await self.bot.send_message(ctx.message.channel, self.bot.bot_prefix + " Error:\n\n%s" % format_exc())

    @commands.command(aliases=['gban'], pass_context=True)
    async def globalban(self, ctx, *, user):
        """Bans the given user from all servers you have permissions to and blocks him."""
        try:
            member = self.get_user(user,ctx.message)
            if not member: await self.bot.send_message(message.channel, "User \"%s\" not found."%user); return
            servers = 0
            block_user(member.id)
            for server in self.bot.servers:
                try:
                    await self.bot.ban(member, delete_message_days=7)
                    servers += 1
                except discord.Forbidden: pass
            if servers > 0:
                await self.bot.send_message(ctx.message.channel, "{} Blocked and banned user: {} from {} servers.".format(self.bot.bot_prefix, member.mention, servers))
            else:
                await self.bot.send_message(ctx.message.channel, "{} No servers to ban user {} from. Only blocked him.".format(self.bot.bot_prefix, member.mention))
        except:
            from traceback import format_exc;await self.bot.send_message(ctx.message.channel, self.bot.bot_prefix + " Error:\n\n%s" % format_exc())

    @commands.command(aliases=['gunban'], pass_context=True)
    async def globalunban(self, ctx, *, user):
        """Unbans the given user from all servers you have permissions to and unblocks him."""
        try:
            member = self.get_user(user,ctx.message)
            if not member: await self.bot.send_message(message.channel, "User \"%s\" not found."%user); return
            servers = 0
            block_user(member.id)
            for server in self.bot.servers:
                try:
                    await self.bot.unban(server, member)
                    servers += 1
                except discord.Forbidden: pass
            if servers > 0:
                await self.bot.send_message(ctx.message.channel, "{} Unbanned user: {} from {} servers.".format(self.bot.bot_prefix, member.mention, servers))
            else:
                await self.bot.send_message(ctx.message.channel, "{} No servers to unban user {} from.".format(self.bot.bot_prefix, member.mention))
        except:
            from traceback import format_exc;await self.bot.send_message(ctx.message.channel, self.bot.bot_prefix + " Error:\n\n%s" % format_exc())

def setup(bot):
    bot.add_cog(globalban(bot))
