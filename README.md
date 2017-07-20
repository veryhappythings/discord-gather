[![Build Status](https://travis-ci.org/veryhappythings/discord-gather.svg?branch=master)](https://travis-ci.org/veryhappythings/discord-gather) [![Coverage Status](https://coveralls.io/repos/github/veryhappythings/discord-gather/badge.svg?branch=master)](https://coveralls.io/github/veryhappythings/discord-gather?branch=master)


## A basic discord bot for Dota 2 pickup games

This is a very lightweight bot for organising pickup games on Discord. It has no tracking and no matchmaking. It simply maintains a queue of players who wish to play and prints out two randomised teams when enough people are signed in.

## To use

* Get your bot a discord token by adding a new app at https://discordapp.com/developers/applications/me and creating your app a bot user
* Add your bot to your guild by constructing a link from this https://discordapp.com/developers/docs/topics/oauth2#adding-bots-to-guilds - The permissions you will need are 3072, so your link will take the form https://discordapp.com/oauth2/authorize?client_id=[your bot id from the link above]&scope=bot&permissions=3072
* Install python 3.5
* `pip install .` - if you intend to edit the code, use `pip install -e .`
* Put your bot's token into config.json (see config.json.example)
* Run `discord-gather`
* Type !help in any Discord channel that the bot resides in for more information.

## Or if you're a Docker kind of person

https://hub.docker.com/r/veryhappythings/discord-gather/ - Stick DG_TOKEN on your environment and off it goes. Very much a WIP, contributions welcome!

## Contributors

A huge thanks to:

* [@zoidbergwill](https://github.com/zoidbergwill)
* [@joshramsbottom](https://github.com/joshramsbottom)
* [@Doezer](https://github.com/Doezer)
