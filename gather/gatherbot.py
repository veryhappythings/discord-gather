# coding: utf8
import logging
import re
import discord
from gather.organiser import Organiser
from gather import commands


logger = logging.getLogger(__name__)


class DiscordAdaptor:
    def __init__(self, token):
        self.token = token
        self.client = discord.Client()

    def run(self):
        self.client.run(self.token)

    def register_on_ready(self, target):
        self.client.on_ready = target

    def register_on_message(self, target):
        self.client.on_message = target

    def register_on_member_update(self, target):
        self.client.on_member_update = target

    def username(self):
        return self.client.user.name

    async def send_message(self, channel, message):
        await self.client.send_message(channel, message)


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
            logger.info('Message received [{0}]: "{1}"'.format(message.channel, message.content))
            for regex, fn in self.actions.values():
                match = re.match(regex, message.content)
                if match:
                    try:
                        await fn(self, message.channel, message.author, message.content, *match.groups())
                    except Exception as e:
                        logger.exception(e)
                        await self.say(message.channel, 'Something went wrong with that command.')
                    break

    async def _member_went_offline(self, before):
        for channel in self.organiser.queues:
            # Ignore channels that aren't on the old member's server
            if channel.server != before.server:
                continue

            # If the member was in the channel's queue, remove it and announce
            if before in self.organiser.queues[channel]:
                logger.info('{0} went offline'.format(before))
                self.organiser.remove(channel, before)
                await self.say(
                    channel,
                    '{0} was signed in but went offline. {1}'.format(
                        before,
                        self.player_count_display(channel)
                    )
                )
                await self.announce_players(channel)

    async def _member_went_afk(self, before):
        for channel in self.organiser.queues:
            if channel.server != before.server:
                continue

            if before in self.organiser.queues[channel]:
                logger.info('{0} went AFK'.format(before))
                self.organiser.remove(channel, before)
                await self.say(
                    channel,
                    '{0} was signed in but went AFK. {1}'.format(
                        before, self.player_count_display(channel))
                )

    async def on_member_update(self, before, after):
        # Handle players going offline
        if before.status == discord.Status.online and after.status == discord.Status.offline:
            self._member_went_offline(before)
        # Handle players going AFK
        elif before.status == discord.Status.online and after.status == discord.Status.idle:
            self._member_went_afk(before)


class DiscordGather:
    def __init__(self, token):
        self.token = token
        self.bot = None
        self.discord = DiscordAdaptor(token)
        self.discord.register_on_ready(self.on_ready)

    def run(self):
        self.discord.run()

    async def on_ready(self):
        self.bot = GatherBot(self.discord.username)
        self.bot.register_message_handler(self.discord.send_message)
        self.bot.register_action('^!help$', commands.bot_help)
        self.bot.register_action('^!(?:add|join|s)$', commands.add)
        self.bot.register_action('^!(?:remove|rem|so)$', commands.remove)
        self.bot.register_action('^!(?:game|status)$', commands.game_status)
        self.bot.register_action('^!(?:reset)$', commands.reset)

        self.discord.register_on_member_update(self.bot.on_member_update)
        self.discord.register_on_message(self.bot.on_message)

        logger.info('Logged in as')
        logger.info(self.bot.username())
        logger.info('------')
