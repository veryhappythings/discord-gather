# coding: utf8
# !/usr/bin/env python3
import locale
import os
import logging
import json
import gettext

from gather import commands
from gather.gatherbot import GatherBot


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s,%(msecs)03d %(levelname)-5.5s [%(name)s] %(message)s",
    )
    try:
        with open('config.json', mode='r+', encoding='utf-8') as f:
            config = json.load(f)
            language = config["language"]
        locale.setlocale(locale.LC_ALL, language)
    except:
        locale.setlocale(locale.LC_ALL, '')

    loc = locale.getlocale()
    filename = "res/messages_%s.mo" % locale.getlocale()[0][0:2]

    try:
        logging.debug("Opening message file %s for locale %s", filename, loc[0])
        trans = gettext.GNUTranslations(open(filename, "rb"))
    except IOError:
        logging.debug("Locale not found. Using default messages")
        trans = gettext.NullTranslations()

    trans.install()

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
    bot.register_action('^!(?:language)', commands.language)
    bot.register_action('^!(?:reset)$', commands.reset)
    bot.run(config['token'])


if __name__ == '__main__':
    main()
