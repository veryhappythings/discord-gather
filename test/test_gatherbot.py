import unittest
from gather.gatherbot import GatherBot


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
        bot.organiser.queues['testchannel'] = {'player1', 'player2'}
        self.assertEqual(
            '(2/10)',
            bot.player_count_display('testchannel')
        )
