import discord
from discord.ext import commands
import aiohttp
import html
import random
import asyncio


class TriviaException(Exception):
    pass

class TriviaQuestion():
    """Represents a trivia question"""
    LETTERS = ['A', 'B', 'C', 'D']
    EMOJIS = ["\N{REGIONAL INDICATOR SYMBOL LETTER A}", "\N{REGIONAL INDICATOR SYMBOL LETTER B}", "\N{REGIONAL INDICATOR SYMBOL LETTER C}", "\N{REGIONAL INDICATOR SYMBOL LETTER D}"]

    def __init__(self, category, question, correct_answer, incorrect_answers, difficulty):
        self.category = html.unescape(category)
        self.question = html.unescape(question)
        self.correct_answer = html.unescape(correct_answer)
        self.incorrect_answers = [html.unescape(x) for x in incorrect_answers]
        self.difficulty = html.unescape(difficulty)
        self.correct_answer_letter = random.choice(TriviaQuestion.LETTERS)
    

    @classmethod
    async def get_trivia(cls, get_url="https://opentdb.com/api.php?amount=1&type=multiple"):
        async with aiohttp.ClientSession() as cs:
            async with cs.get(get_url) as resp:
                question_dict = await resp.json()
                questions = question_dict.get('results')
                if questions:
                    result = questions[0]  # first question
                    return cls(result['category'], result['question'], result['correct_answer'], result['incorrect_answers'], result['difficulty'])
                else:
                    raise TriviaException("Invalid response received from API.")
    
    def check_is_correct(self, given_answer_emoji) -> bool:
        """Takes in an emoji and checks if it's the correct one for the answer"""
        if given_answer_emoji == "\N{REGIONAL INDICATOR SYMBOL LETTER A}" and self.correct_answer_letter == 'A':
            return True
        elif given_answer_emoji == "\N{REGIONAL INDICATOR SYMBOL LETTER B}" and self.correct_answer_letter == 'B':
            return True
        elif given_answer_emoji == "\N{REGIONAL INDICATOR SYMBOL LETTER C}" and self.correct_answer_letter == 'C':
            return True
        elif given_answer_emoji == "\N{REGIONAL INDICATOR SYMBOL LETTER D}" and self.correct_answer_letter == 'D':
            return True
        else:
            return False

    @property
    def embed(self) -> discord.Embed:
        embed = discord.Embed(title=f'Category: {self.category} ({self.difficulty})', description=self.question, color=discord.Color.blue())

        incorrect_answers = self.incorrect_answers.copy()
        random.shuffle(incorrect_answers)

        for letter in TriviaQuestion.LETTERS:
            if letter == self.correct_answer_letter:
                embed.add_field(name=letter, value=self.correct_answer, inline=False)
            else:
                embed.add_field(name=letter, value=incorrect_answers.pop(), inline=False)
        return embed

    async def send_to_channel(self, channel: discord.abc.Messageable) -> discord.Message:
        msg = await channel.send(embed=self.embed)
        for emoji in TriviaQuestion.EMOJIS:
            await msg.add_reaction(emoji)
        return msg
    
    async def send_as_reply(self, message: discord.Message) -> discord.Message:
        msg = await message.reply(embed=self.embed)
        for emoji in TriviaQuestion.EMOJIS:
            await msg.add_reaction(emoji)
        return msg


class Trivia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=['t','triv'], invoke_without_command=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def trivia(self, ctx: commands.Context):
        triviaquestion = await TriviaQuestion.get_trivia()
        msg = await triviaquestion.send_as_reply(ctx.message)
        try:
            reaction, user = await self.bot.wait_for('reaction_add', check=lambda reaction, user: user == ctx.author and reaction.message == msg and reaction.emoji in TriviaQuestion.EMOJIS, timeout=30.0)
            win = triviaquestion.check_is_correct(reaction.emoji)
            if win:
                await msg.reply(f"{triviaquestion.correct_answer_letter} is correct.")
            else:
                await msg.reply(f"Wrong. The correct answer was {triviaquestion.correct_answer_letter}")
        except asyncio.TimeoutError:
            await msg.reply(f"Too slow. The correct answer was {triviaquestion.correct_answer_letter}")


    @commands.group(aliases=['at','atriv'], invoke_without_command=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def atrivia(self, ctx: commands.Context):
        triviaquestion = await TriviaQuestion.get_trivia()
        msg = await triviaquestion.send_as_reply(ctx.message)
        try:
            reaction, user = await self.bot.wait_for('reaction_add', check=lambda reaction, user: reaction.message == msg and reaction.emoji in TriviaQuestion.EMOJIS, timeout=30.0)
            win = triviaquestion.check_is_correct(reaction.emoji)
            if win:
                await msg.reply(f"{triviaquestion.correct_answer_letter} is correct.")
            else:
                await msg.reply(f"Wrong. The correct answer was {triviaquestion.correct_answer_letter}")
        except asyncio.TimeoutError:
            await msg.reply(f"Too slow. The correct answer was {triviaquestion.correct_answer_letter}")


def setup(bot):
    bot.add_cog(Trivia(bot))
