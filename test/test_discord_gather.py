import unittest
from gather.discord_gather import DiscordGather
from .helper import async_test


class TestDiscordGather(unittest.TestCase):
    @async_test
    async def test_on_ready(self):
        bot = DiscordGather('token')
        bot.discord = unittest.mock.Mock()
        bot.discord.username = 'testuser'
        await bot.on_ready()
        self.assertEqual(bot.bot.username, 'testuser')

    def test_on_member_update(self):
        pass
