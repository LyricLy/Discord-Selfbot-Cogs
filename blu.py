import discord, asyncio
from itertools import repeat
from discord.ext import commands
from PythonGists import PythonGists
from cogs.utils.checks import *
from cogs.utils.react import *
from cogs.utils.api import *

class blu:
    voice = None
    def __init__(self, bot):
        self.bot = bot

    async def on_message(self, message):
        lower = message.content.lower()
        if isinstance(message.channel, discord.abc.GuildChannel):
            if message.guild.id == '299293492645986307':
                if lower == '<@'+self.bot.user.id+'> wiki':
                    await self.bot.send_message(message.channel, "<https://github.com/appu1232/Discord-Selfbot/wiki> {p}".format(p=self.bot.bot_prefix))
            if message.guild.id == '295183533423591435':
                if lower in ['plu','blu']:
                    await self.bot.send_message(message.channel, "is garnicht da {p}".format(p=self.bot.bot_prefix))
            if message.guild.id == '212421397098528779':
                if message.author.id == '241225897389064192':
                    if '<@97138137679028224>' in message.content:
                        await self.bot.kick(message.author)
            elif message.guild.id == '295183533423591435':
                if 'pfeife' in lower:
                    if message.author.permissions_in(message.channel).add_reactions:
                        await message.add_reaction('pfeife:324567059658965023')
            elif message.guild.id == '336245676952387604':
                if 'switch' in lower:
                    if message.author.permissions_in(message.channel).add_reactions:
                        await message.add_reaction('switch:337258812903915530')
                if 'kappa' in lower and not ':kappa:' in lower:
                    if message.author.permissions_in(message.channel).add_reactions:
                        await message.add_reaction('kappa:336835095317053440')
        if lower == 'möp':
            if message.author.permissions_in(message.channel).add_reactions:
                await message.add_reaction('\N{REGIONAL INDICATOR SYMBOL LETTER S}')
                await message.add_reaction('\N{REGIONAL INDICATOR SYMBOL LETTER E}')
                if message.author.id == self.bot.user.id:
                    await asyncio.sleep(30)
                    await message.remove_reaction('\N{REGIONAL INDICATOR SYMBOL LETTER S}', self.bot.user)
                    await message.remove_reaction('\N{REGIONAL INDICATOR SYMBOL LETTER E}', self.bot.user)
        # if message.author.id == '295641075924729859':
        #     if message.author.permissions_in(message.channel).add_reactions:
        #         await message.add_reaction('♥')

    @commands.command(aliases=['mr'], pass_context=True)
    async def markread(self, ctx, channel):
        """Marks the specified channel as read."""
        found_channel = find_channel(ctx.message.guild.channels, channel)
        if not found_channel:
            found_channel = find_channel(self.bot.get_all_channels(), channel)
        if found_channel:
            mark_channel_read(found_channel.id, data='{"token":""}')
            await success(self.bot, ctx.message)
            await asyncio.sleep(10)
            await ctx.message.delete()
        else:
            await error(self.bot, ctx.message)
            await ctx.message.channel.send( self.bot.bot_prefix + " Channel not found.")
    """
    @commands.command(pass_context=True)
    async def accept(self, ctx, channel):
        ""Accepts a pending friend request""
        await
    """
    @commands.command(pass_context=True)
    async def functions(self, ctx, txt):
        """Debug"""
        gist_url = PythonGists.Gist(description='', content=str(txt), name='output.txt')
        await ctx.message.channel.send(gist_url)

    @commands.command(pass_context=True)
    async def raw(self, ctx, msgid: int ):
        await ctx.message.delete()
        async for msg in ctx.message.channel.history().filter(lambda m: m.id == msgid).map(lambda m: m.content):
            return await ctx.message.channel.send('``` '+msg+' ```')

    @commands.command(pass_context=True)
    async def raw2(self, ctx, msgid: int ):
        await ctx.message.delete()
        async for msg in ctx.message.channel.history().filter(lambda m: m.id == msgid).map(lambda m: m.clean_content):
            return await ctx.message.channel.send('``` '+msg+' ```')

    @commands.command(pass_context=True)
    async def roleadd(self, ctx, *, txt):
        for role in ctx.message.guild.roles:
            if role.name.lower() == txt.lower():
                successful = 0
                members = ctx.message.guild.members
                await wait(self.bot, ctx.message)
                for member in members:
                    try:
                        await member.add_roles(role)
                        print('Added role \"{}\" to member \"{}\"'.format(role.name, member.name))
                        successful += 1
                    except:
                        print('Unable to add role \"{}\" to member \"{}\"'.format(role.name, member.name))
                        continue
                await self.bot.edit_message(ctx.message, '{}Added role \"{}\" to {}/{} member(s)'.format(self.bot.bot_prefix, role.name, successful, len(members)))
                break

    @commands.command(pass_context=True)
    async def roleremove(self, ctx, *, txt):
        for role in ctx.message.guild.roles:
            if role.name.lower() == txt.lower():
                successful = 0
                members = ctx.message.guild.members
                await wait(self.bot, ctx.message)
                for member in members:
                    try:
                        await member.remove_roles(role)
                        print('Removed role \"{}\" from member \"{}\"'.format(role.name, member.name))
                        successful += 1
                    except:
                        print('Unable to remove role \"{}\" from member \"{}\"'.format(role.name, member.name))
                        continue
                await self.bot.edit_message(ctx.message, '{}Removed role \"{}\" from {}/{} member(s)'.format(self.bot.bot_prefix, role.name, successful, len(members)))
                break

    @commands.command(pass_context=True)
    async def testt(self, ctx):
        if not self.voice: self.voice = await ctx.channel.guild.get_channel(340519588389322753).connect()
        print('connected to %s'%self.voice.channel.name)
        print(dir(self.voice))
        chans = [340519588389322753, 336253620011925505, 336253277492609034, 336253484804603925, 336323927527915530]
        for _ in repeat(None, 10):
            for chan in chans:
                await self.voice.move_to(ctx.channel.guild.get_channel(chan))
                await asyncio.sleep(1)
                print('switched to %s'%self.voice.channel.name)
                'test'

    @commands.command(aliases=['analyze'], pass_context=True)
    async def analyzestring(self, ctx, *, txt):
        _txt = "```py\n"
        txt = sorted(txt.split(' '))
        for item in txt:
            numbers = sum(c.isdigit() for c in item)
            letters = sum(c.isalpha() for c in item)
            uletters = sum(c.isupper() for c in item)
            lletters = sum(c.islower() for c in item)
            spaces  = sum(c.isspace() for c in item)
            others  = len(item) - numbers - letters - spaces
            _txt += "Length: %02d | Numbers: %02d | Letters: %02d (Upper: %02d | Lower: %02d) | Spaces: %02d | Others: %02d\t\"%s\"\n"%(len(item), numbers, letters, uletters, lletters, spaces, others, item)
        await ctx.send(_txt+"\nSmallest: %s (%s) Largest: %s (%s)```"%(min(txt),len(min(txt)), max(txt), len(max(txt))))

    @commands.command(pass_context=True)
    async def getnames(self, ctx):
        await ctx.message.delete()
        lst = set([])
        async for message in ctx.channel.history(limit=2500):
            if message.author.name.islower() and any(str.isdigit(c) for c in message.author.name):
                lst.add(message.author.name)
        lst = list(lst)
        print('=============')
        print(''.join(lst))
        print('=============')

    @commands.command(pass_context=True)
    async def getids(self, ctx):
        await ctx.message.delete()
        lst = set([])
        async for message in ctx.channel.history(limit=2500):
            if message.author.name.islower() and any(str.isdigit(c) for c in message.author.name):
                lst.add(str(message.author.id))
        lst = list(lst)
        print('=============')
        print(' '.join(lst))
        print('=============')
        #self.bot.get_guild(299293492645986307).get_channel(299431230984683520)

def setup(bot):
    bot.add_cog(blu(bot))
