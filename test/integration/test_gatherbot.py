import unittest
from unittest.mock import call
from collections import namedtuple
from gather import commands
from gather.gatherbot import GatherBot
from ..helper import async_test, get_mock_coro


Member = namedtuple('Member', ['name'])
Member.__str__ = lambda self: self.name
Message = namedtuple('Message', ['author', 'channel', 'content'])
Server = namedtuple('Server', ['name'])
Channel = namedtuple('Channel', ['server', 'name'])


class TestGatherBotIntegration(unittest.TestCase):
    def setUp(self):
        self.send_message = get_mock_coro(True)
        self.bot = GatherBot('gatherbot')
        self.bot.register_message_handler(self.send_message)
        self.bot.register_action('^!help$', commands.bot_help)
        self.bot.register_action('^!(?:add|join|s)$', commands.add)
        self.bot.register_action('^!(?:remove|rem|so)$', commands.remove)
        self.bot.register_action('^!(?:game|status)$', commands.game_status)
        self.bot.register_action('^!(?:reset)$', commands.reset)

    @async_test
    async def test_10_players_find_a_game(self):
        server = Server('testserver')
        channel = Channel(server, 'testchannel')
        for i in range(10):
            await self.bot.on_message(
                Message(Member('player{}'.format(i)), channel, '!s'))

        self.send_message.assert_has_calls([
            call(channel, 'You are now signed in, player0. (1/10)'),
            call(channel, 'You are now signed in, player1. (2/10)'),
            call(channel, 'You are now signed in, player2. (3/10)'),
            call(channel, 'You are now signed in, player3. (4/10)'),
            call(channel, 'You are now signed in, player4. (5/10)'),
            call(channel, 'You are now signed in, player5. (6/10)'),
            call(channel, 'You are now signed in, player6. (7/10)'),
            call(channel, 'You are now signed in, player7. (8/10)'),
            call(channel, 'You are now signed in, player8. (9/10)'),
            call(channel, 'You are now signed in, player9. (10/10)')])
        # FIXME: Check that this message better matches a template.
        # The player order is random, so you can't just compare the message
        self.assertTrue(
            self.send_message.mock_calls[-1][1][1].startswith('Game starting!')
        )

    @async_test
    async def test_multiple_servers(self):
        server1 = Server('testserver1')
        server2 = Server('testserver2')
        channel1 = Channel(server1, 'testchannel')
        channel2 = Channel(server2, 'testchannel')
        for i in range(5):
            await self.bot.on_message(
                Message(Member('player{}'.format(i)), channel1, '!s'))
        for i in range(5, 10):
            await self.bot.on_message(
                Message(Member('player{}'.format(i)), channel2, '!s'))

        self.send_message.assert_has_calls([
            call(channel1, 'You are now signed in, player0. (1/10)'),
            call(channel1, 'You are now signed in, player1. (2/10)'),
            call(channel1, 'You are now signed in, player2. (3/10)'),
            call(channel1, 'You are now signed in, player3. (4/10)'),
            call(channel1, 'You are now signed in, player4. (5/10)'),
            call(channel2, 'You are now signed in, player5. (1/10)'),
            call(channel2, 'You are now signed in, player6. (2/10)'),
            call(channel2, 'You are now signed in, player7. (3/10)'),
            call(channel2, 'You are now signed in, player8. (4/10)'),
            call(channel2, 'You are now signed in, player9. (5/10)')])
        self.assertEqual(10, len(self.send_message.mock_calls), self.send_message.mock_calls)
