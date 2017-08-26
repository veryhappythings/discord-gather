# coding: utf8
import logging
import random
from collections import defaultdict


logger = logging.getLogger(__name__)


class NotEnoughPlayersError(Exception):
    pass


class PlayerNotFoundError(Exception):
    pass


class Organiser:
    TEAM_SIZE = 5

    def __init__(self):
        self.queues = defaultdict(lambda: set())
        self.games_count = defaultdict(int)

    def add(self, queue, player):
        self.queues[queue].add(player)

    def remove(self, queue, player):
        try:
            self.queues[queue].remove(player)
        except KeyError:
            raise PlayerNotFoundError()

    def remove_from_all(self, player):
        affected_queues = set()
        for queue in self.queues:
            if player in self.queues[queue]:
                self.queues[queue].remove(player)
                affected_queues.add(queue)
        return affected_queues

    def reset(self, queue):
        self.queues[queue] = set()

    def ready(self, queue):
        return len(self.queues[queue]) >= Organiser.TEAM_SIZE * 2

    def pop_teams(self, queue):
        if len(self.queues[queue]) < Organiser.TEAM_SIZE * 2:
            raise NotEnoughPlayersError('Not enough players!')

        self.games_count[queue] += 1
        candidates = list(self.queues[queue])
        random.shuffle(candidates)
        players = candidates[:Organiser.TEAM_SIZE * 2]
        team_one = players[Organiser.TEAM_SIZE:]
        team_two = players[:Organiser.TEAM_SIZE]
        for player in players:
            self.queues[queue].remove(player)
        return team_one, team_two
