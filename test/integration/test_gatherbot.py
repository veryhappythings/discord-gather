import unittest
from unittest.mock import ANY, call
from collections import namedtuple
from gather import commands
from gather.gatherbot import GatherBot
from ..helper import async_test, get_mock_coro


Message = namedtuple('Message', ['author', 'channel', 'content'])
Channel = namedtuple('Channel', ['name'])


def create_message(player_name, channel_name, content):
    return Message(player_name, Channel(channel_name), content)


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
        for i in range(10):
            await self.bot.on_message(create_message('player{}'.format(i), 'testchannel', '!s'))

        self.send_message.assert_has_calls([
            call(Channel(name='testchannel'), 'You are now signed in, player0. (1/10)'),
            call(Channel(name='testchannel'), 'You are now signed in, player1. (2/10)'),
            call(Channel(name='testchannel'), 'You are now signed in, player2. (3/10)'),
            call(Channel(name='testchannel'), 'You are now signed in, player3. (4/10)'),
            call(Channel(name='testchannel'), 'You are now signed in, player4. (5/10)'),
            call(Channel(name='testchannel'), 'You are now signed in, player5. (6/10)'),
            call(Channel(name='testchannel'), 'You are now signed in, player6. (7/10)'),
            call(Channel(name='testchannel'), 'You are now signed in, player7. (8/10)'),
            call(Channel(name='testchannel'), 'You are now signed in, player8. (9/10)'),
            call(Channel(name='testchannel'), 'You are now signed in, player9. (10/10)')])
        # FIXME: Check that this message better matches a template.
        # The player order is random, so you can't just compare the message
        self.assertTrue(
            self.send_message.mock_calls[-1][1][1].startswith('Game starting!'))
