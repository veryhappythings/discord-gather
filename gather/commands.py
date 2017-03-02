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
     - !game, !status - check current game status
    """
    if bot.organiser.queues[channel]:
        await bot.announce_players(channel)
    else:
        await bot.say(channel, 'No players currently signed in. You can start a game by typing "!add".')
    if bot.afk_organiser.queues[channel]:
        await bot.announce_afk_players(channel)
    else:
        await bot.say(channel, 'No AFK players.')


def format_team(players):
    return '\n '.join(str(p) for p in players)


async def add(bot, channel, author, message):
    """
     - !add, !s, !join - add yourself to the pool
    """
    if author not in bot.organiser.queues[channel] and author not in bot.afk_organiser.queues[channel]:
        bot.organiser.add(channel, author)
        await bot.say(
            channel,
            'You are now signed in, <@{0}>. {1}'.format(
                author.id,
                bot.player_count_display(channel)
            )
        )
    else:
        await bot.say(
            channel,
            'It seems you\'ve already registered, <@{0}>. {1}'.format(
                author.id,
                bot.player_count_display(channel)
            )
        )

    try:
        team_one, team_two = bot.organiser.pop_teams(channel)
        team_one = format_team(team_one)
        team_two = format_team(team_two)
        await bot.say(
            channel,
            'Game starting!\nTeam 1: {}\nTeam 2: {}'.format(team_one, team_two))
    except NotEnoughPlayersError:
        pass


async def remove(bot, channel, author, message):
    """
     - !remove, !so, !rem - remove yourself from the pool
    """
    try:
        bot.organiser.remove(channel, author)
        await bot.say(
            channel,
            'You are now signed out, <@{0}>. {1}'.format(
                author.id,
                bot.player_count_display(channel)
            )
        )
    except PlayerNotFoundError:
        await bot.say(
            channel,
            "Doesn't look like you are signed in. "
            "Try signing in with !add, <@{}>.".format(author.id))


async def reset(bot, channel, author, message):
    """
     - !reset - Empty the pool for this channel
    """
    if channel.permissions_for(author).administrator:
        bot.organiser.reset(channel)
        await bot.say(channel, 'Channel pool reset.')
