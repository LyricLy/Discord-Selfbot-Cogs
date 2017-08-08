import os
import discord
import json
import datetime
import asyncio
from random import randint
from discord.ext import commands

'''Module to react automatically to @everyone pings.'''


class EveryoneReact:
    def __init__(self, bot):
        self.bot = bot
        if not os.path.exists('cogs/utils/everyone_react.json'):
            with open('cogs/utils/everyone_react.json', 'w') as fp:
                json.dump({'first': False}, fp, indent=4)
        with open('cogs/utils/everyone_react.json') as fp:
            react = json.load(fp)
            for k, v in react.items():
                self.word = k
                self.active = v

    emoji_dict = {
    # these arrays are in order of "most desirable". Put emojis that most convincingly correspond to their letter near the front of each array.
        'a': ['🇦', '🅰', '🍙', '🔼', '4⃣'],
        'b': ['🇧', '🅱', '8⃣'],
        'c': ['🇨', '©', '🗜'],
        'd': ['🇩', '↩'],
        'e': ['🇪', '3⃣', '📧', '💶'],
        'f': ['🇫', '🎏'],
        'g': ['🇬', '🗜', '6⃣', '9⃣', '⛽'],
        'h': ['🇭', '♓'],
        'i': ['🇮', 'ℹ', '🚹', '1⃣'],
        'j': ['🇯', '🗾'],
        'k': ['🇰', '🎋'],
        'l': ['🇱', '1⃣', '🇮', '👢', '💷'],
        'm': ['🇲', 'Ⓜ', '📉'],
        'n': ['🇳', '♑', '🎵'],
        'o': ['🇴', '🅾', '0⃣', '⭕', '🔘', '⏺', '⚪', '⚫', '🔵', '🔴', '💫'],
        'p': ['🇵', '🅿'],
        'q': ['🇶', '♌'],
        'r': ['🇷', '®'],
        's': ['🇸', '💲', '5⃣', '⚡', '💰', '💵'],
        't': ['🇹', '✝', '➕', '🎚', '🌴', '7⃣'],
        'u': ['🇺', '⛎', '🐉'],
        'v': ['🇻', '♈', '☑'],
        'w': ['🇼', '〰', '📈'],
        'x': ['🇽', '❎', '✖', '❌', '⚒'],
        'y': ['🇾', '✌', '💴'],
        'z': ['🇿', '2⃣'],
        '0': ['0⃣', '🅾', '0⃣', '⭕', '🔘', '⏺', '⚪', '⚫', '🔵', '🔴', '💫'],
        '1': ['1⃣', '🇮'],
        '2': ['2⃣', '🇿'],
        '3': ['3⃣'],
        '4': ['4⃣'],
        '5': ['5⃣', '🇸', '💲', '⚡'],
        '6': ['6⃣'],
        '7': ['7⃣'],
        '8': ['8⃣', '🎱', '🇧', '🅱'],
        '9': ['9⃣'],
        '?': ['❓'],
        '!': ['❗', '❕', '⚠', '❣'],

        # emojis that contain more than one letter can also help us react
        # letters that we are trying to replace go in front, emoji to use second
        #
        # if there is any overlap between characters that could be replaced,
        # e.g. 💯 vs 🔟, both could replace "10",
        # the longest ones & most desirable ones should go at the top
        # else you'll have "100" -> "🔟0" instead of "100" -> "💯".
        'combination': [['cool', '🆒'],
                        ['back', '🔙'],
                        ['soon', '🔜'],
                        ['free', '🆓'],
                        ['end', '🔚'],
                        ['top', '🔝'],
                        ['abc', '🔤'],
                        ['atm', '🏧'],
                        ['new', '🆕'],
                        ['sos', '🆘'],
                        ['100', '💯'],
                        ['loo', '💯'],
                        ['zzz', '💤'],
                        ['...', '💬'],
                        ['ng', '🆖'],
                        ['id', '🆔'],
                        ['vs', '🆚'],
                        ['wc', '🚾'],
                        ['ab', '🆎'],
                        ['cl', '🆑'],
                        ['ok', '🆗'],
                        ['up', '🆙'],
                        ['10', '🔟'],
                        ['11', '⏸'],
                        ['ll', '⏸'],
                        ['ii', '⏸'],
                        ['tm', '™'],
                        ['on', '🔛'],
                        ['oo', '🈁'],
                        ['!?', '⁉'],
                        ['!!', '‼'],
                        ['21', '📅'],
                        ]
    }

    # used in >react, checks if it's possible to react with the duper string or not

    def has_dupe(duper):
        collect_my_duper = list(filter(lambda x: x != '<' and x != '⃣',
                                       duper))  # remove < because those are used to denote a written out emoji, and there might be more than one of those requested that are not necessarily the same one.  ⃣ appears twice in the number unicode thing, so that must be stripped too...
        return len(set(collect_my_duper)) != len(collect_my_duper)

    # used in >react, replaces e.g. 'ng' with '🆖'
    def replace_combos(react_me):
        for combo in EveryoneReact.emoji_dict['combination']:
            if combo[0] in react_me:
                react_me = react_me.replace(combo[0], combo[1], 1)
        return react_me

    # used in >react, replaces e.g. 'aaaa' with '🇦🅰🍙🔼'
    def replace_letters(react_me):
        for char in "abcdefghijklmnopqrstuvwxyz0123456789!?":
            char_count = react_me.count(char)
            if char_count > 1:  # there's a duplicate of this letter:
                if len(EveryoneReact.emoji_dict[
                           char]) >= char_count:  # if we have enough different ways to say the letter to complete the emoji chain
                    i = 0
                    while i < char_count:  # moving goal post necessitates while loop instead of for
                        if EveryoneReact.emoji_dict[char][i] not in react_me:
                            react_me = react_me.replace(char, EveryoneReact.emoji_dict[char][i], 1)
                        else:
                            char_count += 1  # skip this one because it's already been used by another replacement (e.g. circle emoji used to replace O already, then want to replace 0)
                        i += 1
            else:
                if char_count == 1:
                    react_me = react_me.replace(char, EveryoneReact.emoji_dict[char][0])
        return react_me

    @commands.group(pass_context=True)
    async def everyonereact(self, ctx):
        """Toggles everyone react mode. >help everyonereact for more...

        Reacts to every @everyone message with something. Default is 'first' Change it with >reactword <txt>"""
        if ctx.invoked_subcommand is None:
            self.active = not self.active
            with open('cogs/utils/everyone_react.json', 'w') as fp:
                json.dump({self.word: self.active}, fp, indent=4)
            await ctx.message.channel.send(self.bot.bot_prefix + 'Everyone react set to: `%s`' % self.active)

    @commands.command(pass_context=True)
    async def reactword(self, ctx, *, txt: str):
        """Set text to react with for everyone react. >help everyonereact for more..."""
        self.word = txt
        with open('cogs/utils/everyone_react.json', 'w') as fp:
            json.dump({self.word: self.active}, fp, indent=4)
        await ctx.message.channel.send(self.bot.bot_prefix + 'Everyone react will now react with: %s' % self.word)

    async def on_message(self, message):
        """React to @everyone pings if enabled."""
        if message.mention_everyone and self.active is True:
            msg = self.word.lower()

            reactions = []
            non_unicode_emoji_list = []
            react_me = ""  # this is the string that will hold all our unicode converted characters from msg

            # replace all custom server emoji <:emoji:123456789> with "<" and add emoji ids to non_unicode_emoji_list
            char_index = 0
            while char_index < len(msg):
                react_me += msg[char_index]
                if msg[char_index] == '<':
                    if (char_index != len(msg) - 1) and msg[char_index + 1] == ":":
                        name_end_colon = msg[char_index + 2:].index(':') + char_index
                        id_end = msg[name_end_colon + 2:].index('>') + name_end_colon
                        non_unicode_emoji_list.append(
                            msg[name_end_colon + 3:id_end + 2])  # we add the custom emoji to the list to replace '<' later
                        char_index = id_end + 2  # jump ahead in react_me parse
                    else:
                        raise Exception("Can't react with '<'")
                char_index += 1
            if EveryoneReact.has_dupe(non_unicode_emoji_list):
                raise Exception(
                    "You requested that I react with at least two of the exact same specific emoji. I'll try to find alternatives for alphanumeric text, but if you specify a specific emoji must be used, I can't help.")

            react_me_original = react_me  # we'll go back to this version of react_me if prefer_combine is false but we can't make the reaction happen unless we combine anyway.

            if EveryoneReact.has_dupe(react_me):  # there's a duplicate letter somewhere, so let's go ahead try to fix it.
                react_me = EveryoneReact.replace_letters(react_me)

                if EveryoneReact.has_dupe(react_me):  # check if we were able to solve the dupe
                    react_me = react_me_original
                    react_me = EveryoneReact.replace_combos(react_me)
                    react_me = EveryoneReact.replace_letters(react_me)
                    if EveryoneReact.has_dupe(react_me):  # this failed too, so there's really nothing we can do anymore.
                        raise Exception("Tried a lot to get rid of the dupe, but couldn't. react_me: " + react_me)
                    else:
                        raise Exception("Tried a lot to get rid of the dupe, but couldn't. react_me: " + react_me)

                lt_count = 0
                for char in react_me:
                    if char != "<":
                        if char not in "0123456789":  # these unicode characters are weird and actually more than one character.
                            if char != '⃣':  # </3
                                reactions.append(char)
                        else:
                            reactions.append(self.emoji_dict[char][0])
                    else:
                        reactions.append(discord.utils.get(self.bot.get_all_emojis(), id=non_unicode_emoji_list[lt_count]))
                        lt_count += 1
            else:  # probably doesn't matter, but by treating the case without dupes seperately, we can save some time
                lt_count = 0
                for char in react_me:
                    if char != "<":
                        if char in "abcdefghijklmnopqrstuvwxyz0123456789!?":
                            reactions.append(self.emoji_dict[char][0])
                        else:
                            reactions.append(char)
                    else:
                        reactions.append(discord.utils.get(self.bot.get_all_emojis(), id=non_unicode_emoji_list[lt_count]))
                        lt_count += 1

            await asyncio.sleep(randint(1,3))
            for i in reactions:
                await message.add_reaction(i)
            print('{} - User {}#{} sent an @everyone in channel: {} of server: {}.\nReacted with: {}'.format(datetime.datetime.now().__format__('%x @ %X'), message.author.name, message.author.discriminator, message.channel.name, message.guild.name, self.word))


def setup(bot):
    bot.add_cog(EveryoneReact(bot))
