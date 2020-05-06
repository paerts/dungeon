import typing as t
import random


def walk_into_wall() -> t.AnyStr:
    return random.choice([
        'The wall is not impressed',
        'The wall does not care',
        'Nothing happens',
        'You look around you to see if someone noticed',
        'You feel stupid'
    ])
