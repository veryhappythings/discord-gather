# coding: utf8
import random
from collections import defaultdict


class NotEnoughPlayersError(Exception):
    pass


class PlayerNotFoundError(Exception):
    pass


class Organiser:
    TEAM_SIZE = 6

    def __init__(self):
        self.queues = defaultdict(lambda: set())

    def add(self, queue, player):
        self.queues[queue].add(player)

    def remove(self, queue, player):
        try:
            self.queues[queue].remove(player)
        except KeyError:
            raise PlayerNotFoundError()

    def reset(self, queue):
        self.queues[queue] = set()

    def ready(self, queue, bot):
        if bot.toggable_feats['Premade']:
            return len(self.queues[queue]) >= Organiser.TEAM_SIZE
        else:
            return len(self.queues[queue]) >= Organiser.TEAM_SIZE * 2

    def is_not_ready(self, queue, bot):
        return not self.ready(queue, bot)

    def pop_teams(self, queue):
        if len(self.queues[queue]) < Organiser.TEAM_SIZE * 2:
            raise NotEnoughPlayersError(_('Not enough players!'))

        candidates = list(self.queues[queue])
        random.shuffle(candidates)
        players = candidates[:Organiser.TEAM_SIZE * 2]
        team_one = players[Organiser.TEAM_SIZE:]
        team_two = players[:Organiser.TEAM_SIZE]
        for player in players:
            self.queues[queue].remove(player)
        return team_one, team_two

    def pop_premade(self, queue):
        if len(self.queues[queue]) < Organiser.TEAM_SIZE:
            raise NotEnoughPlayersError(_('Not enough players!'))

        players = list(self.queues[queue])
        for player in players:
            self.queues[queue].remove(player)
        return players
