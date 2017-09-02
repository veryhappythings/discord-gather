# coding: utf8
import logging
import re
from gather.organiser import Organiser


logger = logging.getLogger(__name__)


class GatherBot:
    def __init__(self, username):
        self.username = username
        self.actions = {}
        self.organiser = Organiser()
        self.message_handlers = []

    def register_message_handler(self, handler):
        self.message_handlers.append(handler)

    async def say(self, channel, message):
        for handler in self.message_handlers:
            await handler(channel, message)

    async def say_lines(self, channel, messages):
        for line in messages:
            await self.say(channel, line)

    async def announce_players(self, channel):
        await self.say(
            channel,
            'Currently signed in players {0}: {1}'.format(
                self.player_count_display(channel),
                ', '.join([str(p) for p in self.organiser.queues[channel]])
            )
        )

    def player_count_display(self, channel):
        return '({0}/{1})'.format(
            len(self.organiser.queues[channel]),
            self.organiser.TEAM_SIZE * 2,
        )

    def register_action(self, regex, coro):
        logger.info('Registering action {0}'.format(regex))
        if regex in self.actions:
            logger.info('Overwriting regex {0}'.format(regex))
        self.actions[regex] = (re.compile(regex, re.IGNORECASE), coro)

    async def on_message(self, message):
        if message.author != self.username:
            for regex, fn in self.actions.values():
                match = re.match(regex, message.content)
                if match:
                    logger.info('Message received [{0}]: "{1}"'.format(
                        message.channel,
                        message.content))
                    try:
                        await fn(
                            self,
                            message.channel,
                            message.author,
                            message.content,
                            *match.groups())
                    except Exception as e:
                        logger.exception(e)
                        await self.say(
                            message.channel,
                            'Something went wrong with that command.')
                    break

    async def member_went_offline(self, before):
        affected_channels = self.organiser.remove_from_all(before)
        for channel in affected_channels:
            await self.say(
                channel,
                '{0} was signed in but went offline. {1}'.format(
                    before,
                    self.player_count_display(channel)))
            await self.announce_players(channel)

    async def member_went_afk(self, before):
        affected_channels = self.organiser.remove_from_all(before)
        for channel in affected_channels:
            await self.say(
                channel,
                '{0} was signed in but went AFK. {1}'.format(
                    before, self.player_count_display(channel)))
            await self.announce_players(channel)
