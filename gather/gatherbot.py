# coding: utf8
import logging
import re
import discord
from gather.organiser import Organiser
from gather import commands


logger = logging.getLogger(__name__)


class GatherBot:
    def __init__(self):
        self.actions = {}
        self.organiser = Organiser()
        self.client = discord.Client()

        self.client.on_ready = self.on_ready
        self.client.on_message = self.on_message
        self.client.on_member_update = self.on_member_update

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

    async def on_ready(self):
        logger.info('Logged in as')
        logger.info(self.client.user.name)
        logger.info(self.client.user.id)
        logger.info('------')

        self.username = self.client.user.name

    async def on_member_update(self, before, after):
        # Handle players going offline
        if before.status == discord.Status.online and after.status == discord.Status.offline:
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
        # Handle players going AFK
        elif before.status == discord.Status.online and after.status == discord.Status.idle:
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
