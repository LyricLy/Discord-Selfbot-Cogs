import discord, asyncio
from cogs.utils.checks import *

class blu:

    def __init__(self, bot):
        self.bot = bot
    
    async def on_message(self, message):
        if message.content.lower() in ['plu','blu'] and message.server.id == '295183533423591435':
            await self.bot.send_message(message.channel, "is garnicht da {p}".format(p=self.bot.bot_prefix))
        if message.content.lower() == 'möp':
            if message.author.permissions_in(message.channel).add_reactions:
                await self.bot.add_reaction(message, '\N{REGIONAL INDICATOR SYMBOL LETTER S}')
                await self.bot.add_reaction(message, '\N{REGIONAL INDICATOR SYMBOL LETTER E}')
                if message.author == self.bot.user:
                    await asyncio.sleep(30)
                    await self.bot.remove_reaction(message, '\N{REGIONAL INDICATOR SYMBOL LETTER S}', self.bot.user)
                    await self.bot.remove_reaction(message, '\N{REGIONAL INDICATOR SYMBOL LETTER E}', self.bot.user)
        if 'pfeife' in message.content.lower():
            if message.author.permissions_in(message.channel).add_reactions:
                await self.bot.add_reaction(message, '<:pfeife:324567059658965023>')
        if message.author.id == '295641075924729859':
            if message.author.permissions_in(message.channel).add_reactions:
                await self.bot.add_reaction(message, '♥')
def setup(bot):
    bot.add_cog(blu(bot))
