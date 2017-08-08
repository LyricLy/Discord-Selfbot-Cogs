import discord, asyncio, re, random
from discord.ext import commands
from cogs.utils.checks import *
from datetime import datetime, timedelta

class tatsumaki:
    active = True
    text = ['To confirm, type `' , '➡  |  Tippe `']
    balancetext = ['balance of', '**, **dein Guthaben beträgt 💴 ']
    reptext = [', **you can award more reputation in ', '**, **in deinem Konto sind ']
    repcantext = ['**, **you can award a reputation point!**', '']
    cmds = ['credits ', 'points ']
    cooldown = '**, please cool down! (**'
    tatsu = 172002275412279296
    allowed = False
    member = ''
    def __init__(self, bot):
        self.bot = bot

    async def on_message(self, message):
        if not self.active: return
        if message.author.id == self.bot.user.id:
            if any(s in message.content.lower() for s in self.cmds):
                print('Allowing auto-transaction via Tatsumaki in channel #'+message.channel.name+' on server "'+message.channel.guild.name+'"')
                self.allowed = True
                # await self.bot.delete_message(message)
        elif message.author.id == self.tatsu and self.allowed:
            if not any(x in message.content for x in self.text): return
            captcha = re.findall("`(\d+)`", message.content)[0]
            if captcha:
                msg = await message.channel.send(captcha)
                await msg.delete()
            self.allowed = False

    def check2(self, msg):
        tatsu = msg.channel.guild.get_member(self.tatsu)
        if msg.author == tatsu: return True

    def check(self, msg):
        tatsu = msg.channel.guild.get_member(self.tatsu)
        if not msg.author == tatsu: return False
        if self.cooldown in msg.content:
            return re.findall("\*\*(\d+)\*\*", msg.content)[0]
        return any(x in msg.content.lower() for x in self.balancetext)

    async def credits(self, channel):
        """Returns current Tatsumaki credits"""
        _msg = await channel.send(content='t!credits')
        try: msg = await self.bot.wait_for('message', timeout=15, check=self.check)
        except asyncio.TimeoutError: return False
        await _msg.delete()
        if msg is None: return False
        _content = msg.content
        if _msg.author.permissions_in(_msg.channel).manage_messages: await msg.delete()
        return int(''.join(char for char in _content.split(self.balancetext[0])[-1] if char.isdigit()))

    async def points(self, channel):
        """Returns current Tatsumaki guild points"""
        _msg = await channel.send(content='t!points')
        try: msg = await self.bot.wait_for('message', timeout=15, check=self.check)
        except asyncio.TimeoutError: return False
        await _msg.delete()
        if msg is None: return False
        _content = msg.content
        if _msg.author.permissions_in(_msg.channel).manage_messages: await msg.delete()
        return int(''.join(char for char in _content.split(self.balancetext[0])[-1] if char.isdigit()))

    async def rep(self, channel):
        """Returns next Tatsumaki rep time"""
        _msg = await channel.send(content='t!rep')
        try: msg = await self.bot.wait_for('message', timeout=15, check=self.check2)
        except asyncio.TimeoutError: return False
        await _msg.delete()
        if msg is None: return False
        _content = msg.clean_content
        if _msg.author.permissions_in(_msg.channel).manage_messages: await msg.delete()
        curtime = datetime.now()
        if any(x in _content for x in self.repcantext):
            repstring = '0 hours, 0 minutes and 0 seconds'
        else:
            repstring = _content.split(self.reptext[0])[1][:-3]
        reptime = datetime.strptime(repstring, '%H hours, %M minutes and %S seconds')
        repdelta = timedelta(hours=reptime.hour, minutes=reptime.minute, seconds=reptime.second)
        return [repstring, reptime, repdelta, curtime+repdelta]

    @commands.group(name='tatsumaki', aliases=['tatsu', 't'], pass_context=True)
    async def _tatsumaki(self, ctx):
        """Toggles Tatsumaki auto captcha solving."""
        if ctx.invoked_subcommand is not None: return
        await ctx.message.delete()
        self.active = not self.active
        await ctx.message.channel.send(self.bot.bot_prefix + 'Tatsumaki set to: `%s`' % self.active)

    @_tatsumaki.command(name='check', pass_context=True)
    async def _check(self, ctx, type: str = 'all'):
        """Checks your current credits, guild points and time to next rep"""
        await ctx.message.delete()
        msg = '_Tatsumaki stats_:\n\n'
        if type in ['all', 'credits']:
            credits = await self.credits(ctx.message.channel)
            if credits: msg += 'Global Credits: **{}**\n'.format(credits)
        if type in ['all', 'points']:
            points = await self.points(ctx.message.channel)
            if points: msg += '*{}* Guild Points: **{}**\n'.format(ctx.message.channel.guild.name, points)
        if type in ['all', 'rep']:
            rep = await self.rep(ctx.message.channel)
            if rep: msg += 'Next rep available in: **{}**\nNext Rep available at: **{}'.format(rep[0], rep[3]).partition('.')[0].rstrip()+'**'
        await ctx.message.channel.send(content=msg)

    @_tatsumaki.command(name='giveaway', pass_context=True)
    async def _giveaway(self, ctx, type: str = 'default'):
        """Gives away all your guildpoints, credits and/or rep to randoms on the current guild"""
        await ctx.message.delete()
        online_members = []
        for member in ctx.message.channel.guild.members:
            if not member.status == discord.Status.offline and not member.bot:
                online_members.append(member.id)
        random_member = random.choice(online_members)
        while random_member == self.member:
            random_member = random.choice(online_members)
        tatsu = ctx.message.channel.guild.get_member(self.tatsu)
        type = type.lower()
        if type in ['default', 'all' , 'credits']:
            credits = await self.credits(ctx.message.channel)
            if not credits == '0':
                await asyncio.sleep(5)
                msg = await ctx.message.channel.send('t!credits <@{id}> {credits}'.format(id=random_member, credits=credits))
                # await self.bot.delete_message(msg)
                self.member = random_member
        if type in ['default', 'all', 'points']:
            await asyncio.sleep(5)
            while random_member == self.member:
                random_member = random.choice(online_members)
            points = await self.points(ctx.message.channel)
            if not points == '0':
                await asyncio.sleep(5)
                msg = await ctx.message.channel.send('t!points <@{id}> {points}'.format(id=random_member, points=points))
                # await self.bot.delete_message(msg)
                self.member = random_member
        if type in ['all', 'rep']:
            await asyncio.sleep(3)
            while random_member == self.member:
                random_member = random.choice(online_members)
            msg = await ctx.message.channel.send('t!rep {}'.format(random_member))
            await msg.delete()
            self.member = random_member

def setup(bot):
    bot.add_cog(tatsumaki(bot))
