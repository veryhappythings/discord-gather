#!/usr/bin/env python3
import os
import logging
import json

from gather import gatherbot
from gather.gatherbot import *
from gather import commands


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s,%(msecs)03d %(levelname)-5.5s [%(name)s] %(message)s",
    )

    # FIXME: This is not very tidy and needs re-doing properly
    if 'DG_TOKEN' in os.environ:
        config = {'token': os.environ['DG_TOKEN']}
    else:
        with open('config.json') as f:
            config = json.load(f)

    bot = GatherBot()
    bot.register_action('^'+gatherbot.prompt+'help$', commands.bot_help)
    bot.register_action('^'+gatherbot.prompt+'(?:add|join|s)$', commands.add)
    bot.register_action('^'+gatherbot.prompt+'(?:remove|rem|so)$', commands.remove)
    bot.register_action('^'+gatherbot.prompt+'(?:game|status)$', commands.game_status)
    bot.register_action('^'+gatherbot.prompt+'(?:reset)$', commands.reset)

    bot.run(config['token'])

if __name__ == '__main__':
    main()
