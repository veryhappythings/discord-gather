import random
from collections import defaultdict


class NotEnoughPlayersError(Exception):
    pass


class PlayerNotFoundError(Exception):
    pass


class Organiser:
    def __init__(self, team_size):
        self.team_size = team_size
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

    def ready(self, queue):
        return len(self.queues[queue]) >= self.team_size * 2

    def pop_teams(self, queue):
        if len(self.queues[queue]) < self.team_size * 2:
            raise NotEnoughPlayersError('Not enough players!')

        candidates = list(self.queues[queue])
        random.shuffle(candidates)
        players = candidates[:self.team_size * 2]
        team_one = players[self.team_size:]
        team_two = players[:self.team_size]
        for player in players:
            self.queues[queue].remove(player)
        return team_one, team_two
