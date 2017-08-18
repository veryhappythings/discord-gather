import re
import unittest
from unittest import mock
from .helper import async_test, get_mock_coro
from gather.gatherbot import GatherBot


class TestGatherBotCommands(unittest.TestCase):
    def test_register(self):
        bot = GatherBot('testuser')
        self.assertEqual({}, bot.actions)
        regex = r'^test'
        action = mock.Mock()
        bot.register_action(regex, action)
        self.assertEqual(
            {regex: (re.compile(regex, re.IGNORECASE), action)},
            bot.actions
        )

    def test_overwrite(self):
        bot = GatherBot('testuser')
        self.assertEqual({}, bot.actions)
        regex = r'^test'
        action = mock.Mock()
        bot.register_action(regex, action)

        new_action = mock.Mock()
        bot.register_action(regex, new_action)
        self.assertEqual(
            {regex: (re.compile(regex, re.IGNORECASE), new_action)},
            bot.actions
        )

    @async_test
    async def test_on_message_from_bot(self):
        bot = GatherBot('testuser')
        regex = r'^test'
        action = get_mock_coro(True)
        bot.actions = {regex: (re.compile(regex, re.IGNORECASE), action)}
        mock_message = mock.Mock()
        mock_message.author = 'testuser'
        mock_message.content = 'test'
        await bot.on_message(mock_message)
        action.assert_not_called()

    @async_test
    async def test_on_message_from_other(self):
        bot = GatherBot('testuser')
        regex = r'^test'
        action = get_mock_coro(True)
        bot.actions = {regex: (re.compile(regex, re.IGNORECASE), action)}
        mock_message = mock.Mock()
        mock_message.author = 'anotheruser'
        mock_message.content = 'test'
        await bot.on_message(mock_message)
        self.assertTrue(action.called)


class TestGatherBotMessageHandling(unittest.TestCase):
    @async_test
    async def test_register_and_send(self):
        bot = GatherBot('testuser')
        handler = get_mock_coro(True)

        bot.register_message_handler(handler)
        await bot.say('Test channel', 'Test message')

        self.assertEqual(1, len(bot.message_handlers))
        self.assertTrue(handler.called)


class TestGatherBot(unittest.TestCase):
    def test_player_count_display_with_zero(self):
        bot = GatherBot('testuser')
        bot.organiser.queues['testchannel'] = set()
        self.assertEqual(
            '(0/10)',
            bot.player_count_display('testchannel')
        )

    def test_player_count_display_with_players(self):
        bot = GatherBot('testuser')
        bot.organiser.queues['testchannel'] = set(['player1', 'player2'])
        self.assertEqual(
            '(2/10)',
            bot.player_count_display('testchannel')
        )

    @unittest.mock.patch('gather.organiser.Organiser')
    @async_test
    async def test_say_lines(self, mock_organiser):
        bot = GatherBot('testuser')
        bot.say = get_mock_coro(True)

        await bot.say_lines(
            'test channel',
            [
                'test message 1',
                'test message 2',
            ]
        )

        bot.say.assert_has_calls([
            unittest.mock.call('test channel', 'test message 1'),
            unittest.mock.call('test channel', 'test message 2'),
        ])

    @unittest.mock.patch('gather.organiser.Organiser')
    @async_test
    async def test_announce_players(self, mock_organiser):
        bot = GatherBot('testuser')
        bot.say = get_mock_coro(True)
        bot.player_count_display = unittest.mock.Mock(return_value='(1/10)')
        bot.organiser.queues['test channel'] = set(['mac'])

        await bot.announce_players('test channel')

        bot.say.assert_called_with(
            'test channel',
            'Currently signed in players (1/10): mac'
        )
