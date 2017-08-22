import unittest
from gather.organiser import Organiser, NotEnoughPlayersError, PlayerNotFoundError


class TestOrganiser(unittest.TestCase):
    def test_add(self):
        organiser = Organiser()

        self.assertEqual(set(), organiser.queues['test'])
        organiser.add('test', 'testplayer')
        self.assertEqual(set(['testplayer']), organiser.queues['test'])

    def test_remove(self):
        organiser = Organiser()

        organiser.queues['test'] = set(['testplayer'])
        organiser.remove('test', 'testplayer')
        self.assertEqual(set(), organiser.queues['test'])

    def test_remove_missing_player(self):
        organiser = Organiser()
        self.assertRaises(PlayerNotFoundError, organiser.remove, 'test', 'testplayer')

    def test_reset(self):
        organiser = Organiser()

        organiser.queues['test'] = set(['testplayer'])
        self.assertEqual(set(['testplayer']), organiser.queues['test'])
        organiser.reset('test')
        self.assertEqual(set(), organiser.queues['test'])

    def test_ready(self):
        organiser = Organiser()
        self.assertFalse(organiser.ready('test'))
        for i in range(Organiser.TEAM_SIZE * 2):
            organiser.queues['test'].add('testplayer{0}'.format(i))
        self.assertTrue(organiser.ready('test'))

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
        self.assertEqual(5, len(organiser.queues['test']))

    def test_pop_teams_validates_queue_size(self):
        organiser = Organiser()
        for i in range(Organiser.TEAM_SIZE):
            organiser.queues['test'].add('testplayer{0}'.format(i))
        self.assertRaises(NotEnoughPlayersError, organiser.pop_teams, 'test')
