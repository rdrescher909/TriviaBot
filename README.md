
# Trivia Bot

## About

This Discord bot was created for a class project, and pulls random trivia questions from OpenTDB and presents them to those that request them.

## Running

### Pre-requisites

1) [Python](https://python.org/downloads) (Tested on 3.10.0 but anything 3.7+ should work fine.)
2) [discord.py](https://discordpy.readthedocs.io/en/stable/)
3) [aiohttp](https://docs.aiohttp.org/en/stable/) (Should be installed when discord.py is installed)
4) A Discord bot set up on the [Discord](https://discord.com) developer dashboard with all privileged intents enabled.

#### discord.py and aiohttp can be installed with the following commands

##### macOS/Linux
`python3 -m pip install discord.py aiohttp`

##### Windows
`py -3.10 -m pip install discord.py aiohttp`


### Start the bot

Create a file in the same directory as the `triviabot.py` script named `TOKEN`. Paste the token for the bot you created on the developer portal in this file with no whitespace.

You are now ready to start the bot and enjoy.


## Contributing

I mean, you probably don't want to, but feel free to fork this project and do whatever with it.