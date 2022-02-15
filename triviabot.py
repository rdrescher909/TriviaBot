import discord
from discord.ext import commands
import traceback
import sys

#Read in the bot's token
with open("TOKEN", "r") as fp: TOKEN = fp.read()

PREFIX = "-"  # Command prefix

#Add your extension to this list to have it added to the bot.
extensions = ("cogs.trivia", "cogs.py")

intents = discord.Intents.all()
mem_cache_flags = discord.MemberCacheFlags.all()

bot = commands.Bot(commands.when_mentioned_or(PREFIX), None, intents=intents, member_cache_flags=mem_cache_flags, case_insensitive=True, activity=discord.Game(name="Trivia | -trivia"))

for extension in extensions: #load the extensions
    bot.load_extension(extension)


@bot.event
async def on_command_error(ctx: commands.Context, error):

    cog = ctx.cog
    if cog:
        if cog._get_overridden_method(cog.cog_command_error) is not None:
            return

    ignored = (commands.CommandNotFound, )

    error = getattr(error, 'original', error)

    if isinstance(error, ignored):
        return
    
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"A little too quick there. Try again in {error.retry_after:.1f} seconds.", delete_after=2.0)
    
    else:
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


@bot.command()
@commands.is_owner()
async def update_status(ctx: commands.Context, *, args):
    await bot.change_presence(activity=discord.Game(name=args))
    await ctx.send("Updated status successfully.")


if __name__ == "__main__":
    bot.run(TOKEN)

