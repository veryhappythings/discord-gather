#!/usr/bin/env python3
import os
import logging
import json

from gather import commands
from gather.gatherbot import GatherBot


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
    bot.register_action('^!help$', commands.bot_help)
    bot.register_action('^!(?:add|join|s)$', commands.add)
    bot.register_action('^!(?:remove|rem|so)$', commands.remove)
    bot.register_action('^!(?:game|status)$', commands.game_status)
    bot.register_action('^!(?:toggle)', commands.toggle)
    bot.register_action('^!(?:reset)$', commands.reset)
    bot.run(config['token'])


if __name__ == '__main__':
    main()
