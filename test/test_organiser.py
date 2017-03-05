import unittest
from gather.organiser import Organiser, NotEnoughPlayersError, PlayerNotFoundError
from gather.gatherbot import GatherBot


class TestOrganiser(unittest.TestCase):
    def test_add(self):
        organiser = Organiser()

        self.assertEqual(set(), organiser.queues['test'])
        organiser.add('test', 'testplayer')
        self.assertEqual({'testplayer'}, organiser.queues['test'])

    def test_remove(self):
        organiser = Organiser()

        organiser.queues['test'] = {'testplayer'}
        self.assertEqual({'testplayer'}, organiser.queues['test'])
        organiser.remove('test', 'testplayer')
        self.assertEqual(set(), organiser.queues['test'])

    def test_remove_missing_player(self):
        organiser = Organiser()
        self.assertEqual(set(), organiser.queues['test'])
        self.assertRaises(PlayerNotFoundError, organiser.remove, 'test', 'testplayer')

    def test_reset(self):
        organiser = Organiser()

        organiser.queues['test'] = {'testplayer'}
        self.assertEqual({'testplayer'}, organiser.queues['test'])
        organiser.reset('test')
        self.assertEqual(set(), organiser.queues['test'])

    def test_ready(self):
        organiser = Organiser()
        bot = GatherBot()
        bot.toggable_feats = {'AFK': False, 'Premade': False}
        self.assertFalse(organiser.ready('test', bot))
        for i in range(Organiser.TEAM_SIZE * 2):
            organiser.queues['test'].add('testplayer{0}'.format(i))
        self.assertTrue(organiser.ready('test', bot))

        organiser2 = Organiser()
        bot.toggable_feats = {'AFK': False, 'Premade': True}
        self.assertFalse(organiser2.ready('test', bot))
        for i in range(Organiser.TEAM_SIZE):
            organiser2.queues['test'].add('testplayer{0}'.format(i))
        self.assertTrue(organiser2.ready('test', bot))

    def test_is_not_ready(self):
        organiser = Organiser()
        bot = GatherBot()
        bot.toggable_feats = {'AFK': False, 'Premade': False}
        self.assertTrue(organiser.is_not_ready('test', bot))
        for i in range(Organiser.TEAM_SIZE*2):
            organiser.queues['test'].add('testplayer{0}'.format(i))
        self.assertFalse(organiser.is_not_ready('test', bot))

        organiser2 = Organiser()
        bot.toggable_feats = {'AFK': False, 'Premade': True}
        self.assertTrue(organiser2.is_not_ready('test', bot))
        for i in range(Organiser.TEAM_SIZE):
            organiser2.queues['test'].add('testplayer{0}'.format(i))
        self.assertFalse(organiser2.is_not_ready('test', bot))

    def test_pop_teams(self):
        organiser = Organiser()
        for i in range(Organiser.TEAM_SIZE * 2):
            organiser.queues['test'].add('testplayer{0}'.format(i))
        teams = organiser.pop_teams('test')
        self.assertEqual(Organiser.TEAM_SIZE, len(teams[0]))
        self.assertEqual(Organiser.TEAM_SIZE, len(teams[1]))
        for player in teams[0]:
            self.assertTrue(player not in teams[1])
        for player in teams[1]:
            self.assertTrue(player not in teams[0])
        self.assertEqual(0, len(organiser.queues['test']))

    def test_pop_teams_leaves_extras(self):
        organiser = Organiser()
        for i in range(Organiser.TEAM_SIZE * 3):
            organiser.queues['test'].add('testplayer{0}'.format(i))
        teams = organiser.pop_teams('test')
        self.assertEqual(Organiser.TEAM_SIZE, len(teams[0]))
        self.assertEqual(Organiser.TEAM_SIZE, len(teams[1]))
        self.assertEqual(6, len(organiser.queues['test']))

    def test_pop_teams_validates_queue_size(self):
        organiser = Organiser()
        for i in range(Organiser.TEAM_SIZE):
            organiser.queues['test'].add('testplayer{0}'.format(i))
        self.assertRaises(NotEnoughPlayersError, organiser.pop_teams, 'test')
