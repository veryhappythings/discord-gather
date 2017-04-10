import unittest
from unittest import mock
from .helper import async_test, get_mock_coro
from gather.gatherbot import GatherBot, on_ready, on_message


class TestGatherBot(unittest.TestCase):
    def test_player_count_display_with_zero(self):
        bot = GatherBot()
        bot.organiser.queues['testchannel'] = set()
        self.assertEqual(
            '(0/10)',
            bot.player_count_display('testchannel')
        )

    def test_player_count_display_with_players(self):
        bot = GatherBot()
        bot.organiser.queues['testchannel'] = set(['player1', 'player2'])
        self.assertEqual(
            '(2/10)',
            bot.player_count_display('testchannel')
        )

    @unittest.mock.patch('discord.Client')
    @unittest.mock.patch('gather.organiser.Organiser')
    def test_init(self, mock_organiser, mock_client):
        bot = GatherBot()
        bot.run('testtoken')

        self.assertIsNotNone(bot.organiser)
        self.assertIsNotNone(bot.client)

    @unittest.mock.patch('discord.Client')
    @unittest.mock.patch('gather.organiser.Organiser')
    @async_test
    async def test_say(self, mock_organiser, mock_client):
        bot = GatherBot()
        bot.run('testtoken')
        bot.client.send_message = get_mock_coro(True)

        await bot.say('test channel', 'test message')

        bot.client.send_message.assert_called_with(
            'test channel',
            'test message'
        )

    @unittest.mock.patch('discord.Client')
    @unittest.mock.patch('gather.organiser.Organiser')
    @async_test
    async def test_say_lines(self, mock_organiser, mock_client):
        bot = GatherBot()
        bot.run('testtoken')
        bot.client.send_message = get_mock_coro(True)

        await bot.say_lines(
            'test channel',
            [
                'test message 1',
                'test message 2',
            ]
        )

        bot.client.send_message.assert_has_calls([
            unittest.mock.call('test channel', 'test message 1'),
            unittest.mock.call('test channel', 'test message 2'),
        ])

    @unittest.mock.patch('discord.Client')
    @unittest.mock.patch('gather.organiser.Organiser')
    @async_test
    async def test_announce_players(self, mock_organiser, mock_client):
        bot = GatherBot()
        bot.run('testtoken')
        bot.client.send_message = get_mock_coro(True)
        bot.player_count_display = unittest.mock.Mock(return_value='(1/10)')
        bot.organiser.queues['test channel'] = set(['mac'])

        await bot.announce_players('test channel')

        bot.client.send_message.assert_called_with(
            'test channel',
            'Currently signed in players (1/10): mac'
        )

    @async_test
    async def test_on_ready(self):
        mock_bot = mock.Mock()
        mock_bot.client.user.name = 'testusername'
        mock_bot.client.user.id = 'testuserid'

        await on_ready(mock_bot)

        self.assertEqual('testusername', mock_bot.username)

    @async_test
    async def test_on_message(self):
        mock_bot = mock.Mock()
        mock_bot.on_message = get_mock_coro(None)
        mock_message = mock.Mock(
            channel='testchannel',
            author='testauthor',
            content='testcontent'
        )

        await on_message(mock_bot, mock_message)

        mock_bot.on_message.assert_has_calls([mock.call('testchannel', 'testauthor', 'testcontent')])
