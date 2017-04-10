# coding: utf8
import asyncio
import logging
import functools
import discord
from gather.bot import ListenerBot
from gather.organiser import Organiser


logger = logging.getLogger(__name__)


async def on_ready(self):
    logger.info('Logged in as')
    logger.info(self.client.user.name)
    logger.info(self.client.user.id)
    logger.info('------')

    self.username = self.client.user.name


async def on_message(self, message):
    # FIXME: These are still objects, and perhaps they need to be?
    await self.on_message(message.channel, message.author, message.content)


async def on_member_update(self, before, after):
    if before.status == discord.Status.online and after.status == discord.Status.offline:
        for channel in self.organiser.queues:
            if channel.server != before.server:
                continue

            if before in self.organiser.queues[channel]:
                self.organiser.remove(channel, before)
                await self.say(
                    channel,
                    '{0} was signed in but went offline. {1}'.format(
                        before,
                        self.player_count_display(channel)
                    )
                )
                await self.announce_players(channel)


class GatherBot(ListenerBot):
    def __init__(self):
        super().__init__()

        self.organiser = Organiser()
        self.client = discord.Client()

        self.client.on_ready = asyncio.coroutine(functools.partial(on_ready, self))
        self.client.on_message = asyncio.coroutine(functools.partial(on_message, self))
        self.client.on_member_update = asyncio.coroutine(functools.partial(on_member_update, self))

    def run(self, token):
        self.token = token
        self.client.run(self.token)

    async def say(self, channel, message):
        await self.client.send_message(channel, message)

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
