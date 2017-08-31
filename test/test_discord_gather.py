from collections import namedtuple
import unittest
import discord
from gather.discord_gather import DiscordGather, report
from .helper import async_test, get_mock_coro


class TestDiscordGather(unittest.TestCase):
    @async_test
    async def test_on_ready(self):
        gather = DiscordGather('token')
        gather.client = unittest.mock.Mock()
        gather.client.user.name = 'testuser'
        await gather.on_ready()
        self.assertEqual(gather.bot.username, 'testuser')

    @async_test
    async def test_on_member_update_player_goes_offline(self):
        gather = DiscordGather('token')
        gather.bot = unittest.mock.Mock()
        gather.bot.member_went_offline = get_mock_coro(True)
        before = unittest.mock.Mock()
        before.status = discord.Status.online
        after = unittest.mock.Mock()
        after.status = discord.Status.offline
        await gather.on_member_update(before, after)
        self.assertTrue(gather.bot.member_went_offline.called)

    @async_test
    async def test_on_member_update_player_goes_afk(self):
        gather = DiscordGather('token')
        gather.bot = unittest.mock.Mock()
        gather.bot.member_went_afk = get_mock_coro(True)
        before = unittest.mock.Mock()
        before.status = discord.Status.online
        after = unittest.mock.Mock()
        after.status = discord.Status.idle
        await gather.on_member_update(before, after)
        self.assertTrue(gather.bot.member_went_afk.called)

    def test_report(self):
        organiser = unittest.mock.Mock()
        MockChannel = namedtuple('Channel', ['server'])
        key = MockChannel('testserver')
        organiser.queues = {
            key: ['player1']
        }
        organiser.games_count = {
            key: 1
        }

        self.assertEqual("Report:\ntestserver-Channel(server='testserver'): 1 current players - 1 games to date", report(organiser))
