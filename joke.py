import requests, discord, json
from discord.ext import commands

'''Joke generator.'''


class JokeGenerator:

    def __init__(self, bot):
        self.bot = bot


    @commands.command(pass_context=True)
    async def joke(self, ctx):
        """Returns a random Joke from https://tambalapi.herokuapp.com via https://github.com/KiaFathi/tambalAPI"""
        response = json.loads(requests.get("https://tambalapi.herokuapp.com").text)
        await self.bot.send_message(ctx.message.channel, "{}{}".format(self.bot.bot_prefix, response[0]["joke"]))
        await self.bot.delete_message(ctx.message)


    @commands.command(pass_context=True)
    async def chuck(self, ctx):
        """Returns a random Chuck Norris joke from http://www.icndb.com/api/"""
        response = requests.get("http://api.icndb.com/jokes/random").text
        await self.bot.send_message(ctx.message.channel, "{}{}".format(self.bot.bot_prefix, json.loads(response)["value"]["joke"]))
        await self.bot.delete_message(ctx.message)


def setup(bot):
    bot.add_cog(JokeGenerator(bot))