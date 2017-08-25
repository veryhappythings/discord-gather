import logging
import discord
from .discord_adaptor import DiscordAdaptor
from .gatherbot import GatherBot
from . import commands


logger = logging.getLogger(__name__)


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

        self.discord.register_on_member_update(self.on_member_update)
        self.discord.register_on_message(self.bot.on_message)

        logger.info('Logged in as')
        logger.info(self.bot.username)
        logger.info('------')

    async def on_member_update(self, before, after):
        # Handle players going offline
        if before.status == discord.Status.online and after.status == discord.Status.offline:
            await self.bot.member_went_offline(before)
        # Handle players going AFK
        elif before.status == discord.Status.online and after.status == discord.Status.idle:
            await self.bot.member_went_afk(before)
