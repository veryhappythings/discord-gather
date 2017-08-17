# coding: utf8
import asyncio
import logging
import functools
import re
import discord
from gather.organiser import Organiser
from gather import commands


logger = logging.getLogger(__name__)


async def on_ready(bot):
    logger.info('Logged in as')
    logger.info(bot.client.user.name)
    logger.info(bot.client.user.id)
    logger.info('------')

    bot.username = bot.client.user.name


async def on_message(bot, message):
    # FIXME: These are still objects, and perhaps they need to be?
    await bot.on_message(message.channel, message.author, message.content)


async def on_member_update(bot, before, after):
    # Handle players going offline
    if before.status == discord.Status.online and after.status == discord.Status.offline:
        for channel in bot.organiser.queues:
            # Ignore channels that aren't on the old member's server
            if channel.server != before.server:
                continue

            # If the member was in the channel's queue, remove it and announce
            if before in bot.organiser.queues[channel]:
                logger.info('{0} went offline'.format(before))
                bot.organiser.remove(channel, before)
                await bot.say(
                    channel,
                    '{0} was signed in but went offline. {1}'.format(
                        before,
                        bot.player_count_display(channel)
                    )
                )
                await bot.announce_players(channel)
    # Handle players going AFK
    elif before.status == discord.Status.online and after.status == discord.Status.idle:
        for channel in bot.organiser.queues:
            if channel.server != before.server:
                continue

            if before in bot.organiser.queues[channel]:
                logger.info('{0} went AFK'.format(before))
                bot.organiser.remove(channel, before)
                await bot.say(
                    channel,
                    '{0} was signed in but went AFK. {1}'.format(
                        before, bot.player_count_display(channel))
                )


class GatherBot:
    def __init__(self):
        self.actions = {}
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


class DiscordGather:
    def __init__(self, token):
        self.token = token

        self.bot = GatherBot()
        self.bot.register_action('^!help$', commands.bot_help)
        self.bot.register_action('^!(?:add|join|s)$', commands.add)
        self.bot.register_action('^!(?:remove|rem|so)$', commands.remove)
        self.bot.register_action('^!(?:game|status)$', commands.game_status)
        self.bot.register_action('^!(?:reset)$', commands.reset)

    def run(self):
        self.bot.run(self.token)
