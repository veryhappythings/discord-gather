#!/usr/bin/env python3
import logging
import discord
from gather.bot import ListenerBot
from gather.organiser import Organiser


logger = logging.getLogger(__name__)

prompt = "£"


class GatherBot(ListenerBot):
    def __init__(self):
        super().__init__()
        self.organiser = Organiser()
        self.afk_organiser = Organiser()
        self.client = discord.Client()

        @self.client.event
        async def on_ready():
            logger.info('Logged in as')
            logger.info(self.client.user.name)
            logger.info(self.client.user.id)
            logger.info('------')

            self.username = self.client.user.name

        @self.client.event
        async def on_message(message):
            # FIXME: These are still objects, and perhaps they need to be?
            await self.on_message(message.channel, message.author, message.content)

        @self.client.event
        async def on_member_update(before, after):
            if before.status == discord.Status.online and after.status == discord.Status.offline:
                for channel in self.organiser.queues:
                    if channel.server != before.server:
                        continue

                    if before in self.organiser.queues[channel]:
                        self.organiser.remove(channel, before)
                        await self.say(
                            channel,
                            '<@{0}> s\était inscrit mais s\'est déconnecté. {1}'.format(
                                before.id,
                                self.player_count_display(channel)
                            )
                        )
                        await self.announce_players(channel)

            # If the user passes in idle mode (AFK)
            elif before.status == discord.Status.online and after.status == discord.Status.idle:
                for channel in self.organiser.queues:

                    if channel.server != before.server:
                        continue

                    # if the user is added then we remove him from the current PUG and keep him aside in afk_organiser
                    if before in self.organiser.queues[channel]:
                        self.organiser.remove(channel, before)
                        self.afk_organiser.add(channel, before)
                        await self.say(
                            channel,
                            '{0} s\était inscrit mais est passé AFK. {1}'.format(
                                before.nick,
                                self.player_count_display(channel)
                            )
                        )
                        await self.announce_players(channel)

            # If user was AFK and comes back online
            elif before.status == discord.Status.idle and after.status == discord.Status.online:
                for channel in self.organiser.queues:

                    if channel.server != before.server:
                        continue

                    # If the user was AFK before, and that the current PUG is not ready, then add it again
                    if before in self.afk_organiser.queues[channel] & self.organiser.is_not_ready(channel):
                        self.afk_organiser.remove(channel, before)
                        self.organiser.add(channel, before)
                        await self.say(
                            channel,
                            '{0} était passé AFK après s\'être inscrit. Il repasse dans la file d\'attente. {1}'.format(
                                before.nick,
                                self.player_count_display(channel)
                            )
                        )
                        await self.announce_players(channel)

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
            'Nombe de joueurs actuellement inscrits {0}: {1}'.format(
                self.player_count_display(channel),
                ', '.join([str(p) for p in self.organiser.queues[channel]])
            )
        )

    async def announce_afk_players(self, channel):
        await self.say(
            channel,
            'Nombe de joueurs actuellement inscrits {0}: {1}'.format(
                self.player_count_display(channel),
                ', '.join([str(p) for p in self.afk_organiser.queues[channel]])
            )
        )

    def player_count_display(self, channel):
        return '({0}/{1})'.format(
            len(self.organiser.queues[channel]),
            self.organiser.TEAM_SIZE * 2,
        )
