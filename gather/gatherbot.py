import logging
import discord
from gather.bot import ListenerBot
from gather.organiser import Organiser


logger = logging.getLogger(__name__)


class GatherBot(ListenerBot):
    def __init__(self, team_size):
        super().__init__()

        self.organiser = Organiser(team_size)
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
            'Currently signed in players ({0}/{1}): {2}.'.format(
                len(self.organiser.queues[channel]),
                self.organiser.team_size * 2,
                ', '.join([str(p) for p in self.organiser.queues[channel]])
            )
        )
