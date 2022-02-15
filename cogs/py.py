"""
Copyright 2021 Robert Drescher

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy,
modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software
is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT
OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from discord.ext import commands
from discord import embeds
from discord.utils import get
import discord
import math
from io import StringIO
import sys
import typing
import random
import asyncio


class PyTest(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.command(aliases=['ex', 'exec'])
    @commands.is_owner()
    async def py(self, cntx: commands.Context, *, code):
        """
            Takes in a string of code in 
            ```python
               CODE``` 

            or
            ```
            CODE
            ```

            or 

            CODE


            format and runs it, stripping the leading and trailing markdown in the process, if applicable.
        """
        try:
            old_stdout = sys.stdout
            sys.stdout = mystdout = StringIO() #will hold the output of the code run

            bot: commands.Bot = self.bot
            ctx = cntx
            async with cntx.channel.typing():
                if code.startswith("```python") and code.endswith("```"):
                    code = code[10:-3]
                elif code.startswith("```py") and code.endswith("````"):
                    code = code[5:-3]
                elif code.startswith("```") and code.endswith("```"):
                    code = code[3:-3]
                else:
                    code = code

                async def aexec(code, cntx):
                    ldict = {}
                    bot = self.bot
                    ctx = cntx
                    #Need to make a coro to run it so you can make async calls
                    exec(f'async def __ex(): ' + ''.join(f'\n {l}' for l in code.split('\n')), {"discord": discord, "random": random, "commands": commands, "embeds": embeds, "get": get, "math": math, 'ctx': cntx, 'cntx': cntx, 'bot': bot, 'asyncio': asyncio}, ldict)
                    return await ldict['__ex']() #await the created coro
                await asyncio.wait_for(aexec(code, cntx), timeout=600) #Should time it out after 360 seconds
                # await aexec(code, cntx)
                await cntx.message.add_reaction("\N{WHITE HEAVY CHECK MARK}")
        finally:
            sys.stdout = old_stdout
            if mystdout.getvalue():
                paginator = commands.Paginator(max_size=2000)
                for line in mystdout.getvalue().split("\n"):
                    paginator.add_line(line)
                for page in paginator.pages:
                    await cntx.send(page)

    @py.error
    async def err_handler(self, cntx, error):
        await cntx.send(f"```{error}```")
        await cntx.message.add_reaction("\N{CROSS MARK}")


def setup(bot):
    bot.add_cog(PyTest(bot))

