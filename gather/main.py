#!/usr/bin/env python3
# coding: utf8
import os
import logging
import json
from gather.discord_gather import DiscordGather


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

    bot = DiscordGather(config['token'])
    bot.run()

if __name__ == '__main__':
    main()
