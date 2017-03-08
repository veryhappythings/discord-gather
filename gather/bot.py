# coding: utf8
import logging
import re


logger = logging.getLogger(__name__)


class ListenerBot:
    """ Abstract bot that understands the idea of listening for a message and
    calling a function based on the contents of the message.

    Not sure if this is a useful abstraction, but it does allow for easy testing
    of this code.
    """

    def __init__(self):
        self.actions = {}
        self.username = None

    def register_action(self, regex, coro):
        logger.info('Registering action {0}'.format(regex))
        if regex in self.actions:
            logger.info('Overwriting regex {0}'.format(regex))
        self.actions[regex] = (re.compile(regex, re.IGNORECASE), coro)

    async def on_message(self, channel, author, content):
        if author != self.username:
            logger.info('Message received [{0}]: "{1}"'.format(channel, content))
            for regex, fn in self.actions.values():
                match = re.match(regex, content)
                if match:
                    try:
                        await fn(self, channel, author, content, *match.groups())
                    except Exception as e:
                        logger.exception(e)
                        await self.say(channel, 'Something went wrong with that command.')
                    break

    async def say(self, channel, message):
        pass
