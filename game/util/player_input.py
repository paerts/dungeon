import typing as t


class PlayerCommands:
    UNKNOWN = 'unknown'
    PLAYER_QUIT = 'player_quit'
    PLAYER_UP = 'UP'
    PLAYER_DOWN = 'DOWN'
    PLAYER_LEFT = 'LEFT'
    PLAYER_RIGHT = 'RIGHT'
    SHOW_BACKPACK = 'show_backpack'


def _get_player_input(prompt: t.AnyStr) -> t.AnyStr:
    command = input(prompt)
    return command


def _translate_player_input(player_input: t.AnyStr) -> t.AnyStr:
    """
    >>> _translate_player_input('w')
    'player_up'
    >>> _translate_player_input('s')
    'player_down'
    >>> _translate_player_input('a')
    'player_left'
    >>> _translate_player_input('d')
    'player_right'
    >>> _translate_player_input('q')
    'player_quit'
    >>> _translate_player_input('W')
    'player_up'
    >>> _translate_player_input('foo')
    'unknown'
    """
    player_input = player_input.lower()

    if player_input in ['w']:
        return PlayerCommands.PLAYER_UP

    if player_input in ['s']:
        return PlayerCommands.PLAYER_DOWN

    if player_input in ['a']:
        return PlayerCommands.PLAYER_LEFT

    if player_input in ['d']:
        return PlayerCommands.PLAYER_RIGHT

    if player_input in ['b']:
        return PlayerCommands.SHOW_BACKPACK

    if player_input in ['q']:
        return PlayerCommands.PLAYER_QUIT

    return PlayerCommands.UNKNOWN


def get_player_command(prompt: t.AnyStr = '> ') -> t.AnyStr:
    player_command = _translate_player_input(_get_player_input(prompt))
    if player_command != PlayerCommands.UNKNOWN:
        return player_command

    while player_command == PlayerCommands.UNKNOWN:
        print("I don't understand what you mean")
        player_command = _translate_player_input(_get_player_input(prompt))

    return player_command


