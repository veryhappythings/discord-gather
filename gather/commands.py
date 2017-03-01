#!/usr/bin/env python3
import discord

from gather.organiser import NotEnoughPlayersError, PlayerNotFoundError


def strip_help(bot):
    messages = []

    for regex, action in bot.actions.values():
        if action.__doc__:
            messages.append(action.__doc__.strip())
    return messages


async def bot_help(bot, channel, author, message):
    await bot.say_lines(channel, strip_help(bot))


async def game_status(bot, channel, author, message):
    """
     - !game, !status - Permet de connaître le statut du PUG en cours.
    """
    if bot.organiser.queues[channel]:
        await bot.announce_players(channel)
    else:
        await bot.say(channel, 'Aucun joueur inscrit pour le moment. Commencez un PUG en tapant "!add".')


def format_team(players):
    return '\n '.join(str(p) for p in players)


async def add(bot, channel, author, message):
    """
     - !add, !s, !join - Permet de s'inscrire au prochain PUG.
    """
    bot.organiser.add(channel, author)
    await bot.say(
        channel,
        'Tu es maintenant inscrit, {0}. {1}'.format(
            author,
            bot.player_count_display(channel)
        )
    )

    try:
        team_one, team_two = bot.organiser.pop_teams(channel)
        team_one = format_team(team_one)
        team_two = format_team(team_two)
        await bot.say(
            channel,
            'Le PUG peut démarrer !\nTeam 1 : {}\nTeam 2 : {}'.format(team_one, team_two))
    except NotEnoughPlayersError:
        pass


async def remove(bot, channel, author, message):
    """
     - !remove, !so, !rem - Permet de se désinscrire du PUG actuel.
    """
    try:
        bot.organiser.remove(channel, author)
        await bot.say(
            channel,
            'Tu es maintenant désinscrit, {0}. {1}'.format(
                author,
                bot.player_count_display(channel)
            )
        )
    except PlayerNotFoundError:
        await bot.say(
            channel,
            "On dirait tu n'étais pas inscrit. "
            "Essaye en tapant !add, {}.".format(author))


async def reset(bot, channel, author, message):
    """
     - !reset - Réinitialise le PUG en cours.
    """
    if channel.permissions_for(author).administrator:
        bot.organiser.reset(channel)
        await bot.say(channel, 'PUG réinitialisé.')
