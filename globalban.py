import discord, asyncio, requests
from discord.ext import commands
from cogs.utils.checks import *

# noinspection PyStatementEffect,PyUnreachableCode
class globalban:

    def __init__(self, bot):
        self.bot = bot

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

            client.run('MzI5MjI2NTA2MTEzMTIyMzA0.DDPXnw.UMN_crUM-UX2233jnXmCvyP55cc')
            return client.get_user_info(int(user))"""
            return False
        except:
            pass

    def block_user(self, id):
        payload = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.157 Chrome/58.0.3029.110 Discord Canary/1.7.1 Safari/537.36',
            # 'authority': 'canary.discordapp.com',
            'authorization': 'MzI5MjI2NTA2MTEzMTIyMzA0.DDPXnw.UMN_crUM-UX2233jnXmCvyP55cc'
        }
        r = requests.put("https://canary.discordapp.com/api/v6/users/@me/relationships/"+id, data=payload)
        msg = "Requested https://canary.discordapp.com/api/v6/users/@me/relationships/"+id
        msg += "\nStatus: %s" % r.status_code
        msg += "\nContent: %s" % r.content
        return msg

    def unblock_user(self, id):
        payload = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.157 Chrome/58.0.3029.110 Discord Canary/1.7.1 Safari/537.36',
            # 'authority': 'canary.discordapp.com',
            'authorization': 'MzI5MjI2NTA2MTEzMTIyMzA0.DDPXnw.UMN_crUM-UX2233jnXmCvyP55cc'
        }
        r = requests.delete("https://canary.discordapp.com/api/v6/users/@me/relationships/"+id, data=payload)
        msg = "Requested https://canary.discordapp.com/api/v6/users/@me/relationships/"+id
        msg += "\nStatus: %s" % r.status_code
        msg += "\nContent: %s" % r.content
        return msg

    @commands.command(aliases=['fu'], pass_context=True)
    async def finduser(self, ctx, *, user):
        try:
            member = self.get_user(user,ctx.message)
            if not member: await self.bot.send_message(message.channel, "User \"%s\" not found."%user); return
            await self.bot.send_message(ctx.message.channel, "User found: %s" % member.name)
        except:
            from traceback import format_exc;await self.bot.send_message(ctx.message.channel, self.bot.bot_prefix + " Error:\n\n%s" % format_exc())

    @commands.command(aliases=['bl'], pass_context=True)
    async def block(self, ctx, *, user):
        try:
            member = self.get_user(user,ctx.message)
            block = self.block_user(member.id)
            await self.bot.send_message(ctx.message.channel, block)
        except:
            from traceback import format_exc;await self.bot.send_message(ctx.message.channel, self.bot.bot_prefix + " Error:\n\n%s" % format_exc())

    @commands.command(aliases=['gban'], pass_context=True)
    async def globalban(self, ctx, *, user):
        try:
            member = self.get_user(user,ctx.message)
            if not member: await self.bot.send_message(message.channel, "User \"%s\" not found."%user); return
            servers = 0
            # TODO Blocking
            for server in self.bot.servers:
                try:
                    await self.bot.ban(member, delete_message_days=7)
                    servers += 1
                except discord.Forbidden: pass
            if servers > 0:
                await self.bot.send_message(ctx.message.channel, "{} Banned user: {} from {} servers.".format(self.bot.bot_prefix, member.mention, servers))
            else:
                await self.bot.send_message(ctx.message.channel, "{} No servers to ban user {} from.".format(self.bot.bot_prefix, member.mention))
        except:
            from traceback import format_exc;await self.bot.send_message(ctx.message.channel, self.bot.bot_prefix + " Error:\n\n%s" % format_exc())

    @commands.command(aliases=['gunban'], pass_context=True)
    async def globalunban(self, ctx, *, user):
        try:
            member = self.get_user(user,ctx.message)
            if not member: await self.bot.send_message(message.channel, "User \"%s\" not found."%user); return
            servers = 0
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
