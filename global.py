import discord, asyncio, requests, os
from discord.ext import commands
# from cogs.utils.checks import *
from cogs.utils.checksblu import get_user, bool
from cogs.utils.react import *
from cogs.utils.api import *

class UserInteractionRequiredException(Exception): pass

# noinspection PyStatementEffect,PyUnreachableCode
class globalban:

    def __init__(self, bot):
        self.bot = bot
        # raise UserInteractionRequiredException('\nATTENTION: This cog may contain bugs and is only intended to be used by advanced users.\nRemove line 13 from cogs/globalban.py to use this cog!')




    @commands.command(aliases=['pro'], pass_context=True)
    async def profile(self, ctx, *, user: int):
        """Debug command. Shows profile information for the selected user."""
        try:
            member = await self.bot.get_user_profile(user)
            if not member: return await ctx.send("User \"%s\" not found."%user)
            _msg = "%s#%s (%s)" % (member.user.name, member.user.discriminator, member.user.id)
            _msg += "\nNitro: %s" % member.nitro
            if member.premium: _msg += " (Since %s)"% member.premium_since
            _msg += "\nHypeSquad: %s" % member.hypesquad
            _msg += "\nPartner: %s" % member.partner
            _msg += "\nStaff: %s" % member.staff
            await ctx.send(_msg)
        except:
            from traceback import format_exc;await ctx.send(self.bot.bot_prefix + " Error:\n\n%s" % format_exc())


    @commands.command(aliases=['fu'], pass_context=True)
    async def finduser(self, ctx, *, user):
        """Debug command. Checks if we could find the user you're searching for."""
        try:
            member = get_user(user,ctx.message,self.bot)
            if not member: return await ctx.send("User \"%s\" not found."%user)
            _msg = "User found: %s#%s (%s)" % (member.name, member.discriminator, member.id)
            if hasattr(member, 'guild'):
                _msg += "\nMember of guild: %s (%s)" % (member.guild.name, member.guild.id)
            await ctx.send(_msg, embed=discord.Embed(description=member.mention))
        except:
            from traceback import format_exc;await ctx.send(self.bot.bot_prefix + " Error:\n\n%s" % format_exc())

    @commands.command(aliases=['bl'], pass_context=True)
    async def block(self, ctx, *, user):
        """Blocks the user you provide."""
        try:
            member = get_user(user,ctx.message)
            block_user(str(member.id))
            await success(ctx.message)
            await asyncio.sleep(5)
            await ctx.message.delete()
        except:
            from traceback import format_exc;await ctx.send(self.bot.bot_prefix + " Error:\n\n%s" % format_exc())

    @commands.command(aliases=['ubl'], pass_context=True)
    async def unblock(self, ctx, *, user):
        """Unblocks the user you provide."""
        try:
            member = get_user(user,ctx.message)
            unblock_user(str(member.id))
            await success(ctx.message)
            await asyncio.sleep(5)
            await ctx.message.delete()
        except:
            from traceback import format_exc;await ctx.send(self.bot.bot_prefix + " Error:\n\n%s" % format_exc())

    @commands.group(aliases=['global'], pass_context=True)
    async def mass(self, ctx):
        """Allows several actions to be applied on multiple guilds."""
        pass

    @mass.command(pass_context=True)
    async def ban(self, ctx, *, users: str):
        """
        Bans the given user ids from all guilds you have permissions to and blocks him.
        Example: >global ban 344212162329444362 344222162221006868 344223165062578181|Test Reason
        :param ctx:
        :param users:
        :return:
        """
        reason = None
        if "|" in users:
            users = users.split('|')
            reason = users[1]
            users = users[0].split(' ')
        else: users = users.split(' ')
        try: await ctx.message.add_reaction('⌛')
        except: pass
        for user in users: block_user(user)
        guilds = 0
        for guild in self.bot.guilds:
            if guild.me.guild_permissions.ban_members:
                for user in users:
                    try:
                        if reason: request = ban(str(guild.id), user, delete_message_days=7, reason="Globally banned by "+self.bot.user.name+"#"+str(self.bot.user.discriminator)+" for "+reason)
                        else: request = ban(guild.id, user, delete_message_days=7, reason="Globally banned by "+self.bot.user.name+"#"+self.bot.user.discriminator)
                        if request.status_code == 403:
                            print("Insufficient permissions to ban user: " + user + " from guild: " + guild.name); continue
                        elif not request.status_code == 204:
                            print("Unknown Error while trying to ban "+ user + " from guild: " + guild.name); continue
                        print("Banned \"%s\" from \"%s\"" % (user, guild.name))
                    except: print("Unable to ban user: " + user + " from guild: " + guild.name)
                guilds += 1
            elif guild.me.guild_permissions.kick_members:
                print('could kick from %s'%guild.name)
        if guilds > 0:
            text = ":hammer: Blocked and banned users: `{}` from **{}** guilds".format(', '.join(users), guilds)+"" if reason else "."
            if reason: text += " for \"{}\"".format(reason)
        else:
            text = ":hammer: No guilds to ban users `{}` from. Only blocked them.".format(', '.join(users))
        await ctx.message.edit(content=text)
        try: await ctx.message.remove_reaction('⌛', ctx.guild.me)
        except: pass

    @mass.command(pass_context=True)
    async def unban(self, ctx, *, users):
        """
        Unbans the given user from all guilds you have permissions to and unblocks him.
        Example: >global unban 344212162329444362 344222162221006868 344223165062578181
        :param ctx:
        :param users:
        :return:
        """
        users = users.split(' ')
        try: await ctx.message.add_reaction('⌛')
        except: pass
        for user in users: unblock_user(user)
        guilds = 0
        for guild in self.bot.guilds:
            if not guild.me.guild_permissions.ban_members: continue
            for user in users:
                try:
                    request = unban(guild.id, user)
                    if request.status_code == 403:
                        print("Insufficient permissions to unban user: " + user + " from guild: " + guild.name); continue
                    elif not request.status_code == 204:
                        print("Unknown Error while trying to unban "+ user + " from guild: " + guild.name); continue
                    print("Unbanned \"%s\" from \"%s\"" % (user, guild.name))
                except: print("Unable to unban user: " + user + " from guild: " + guild.name)
            guilds += 1
        if guilds > 0:
            text = ":hammer: Unblocked and unbanned users: `{}` from **{}** guilds.".format(', '.join(users), guilds)
        else:
            text = ":hammer: No guilds to unban users `{}` from. Only unblocked them.".format(', '.join(users))
        await ctx.message.edit(content=text)
        try: await ctx.message.remove_reaction('⌛', ctx.guild.me)
        except: pass

def setup(bot):
    bot.add_cog(globalban(bot))
