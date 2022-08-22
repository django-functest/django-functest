import itertools
from typing import Any

from ..models import User

# Factory utils:


class _Auto:
    """
    Sentinel value (used instead of None because that can be a valid value)
    """

    def __bool__(self):
        return False

    def __repr__(self):
        return "<Auto>"


Auto: Any = _Auto()


def str_sequence(template: str, start_at: int = 0):
    """
    Makes a sequence of strings using an integer substution, counting from start_at.
    """
    return (template.format(idx) for idx in itertools.count())


# User factory:

USERNAME_SEQUENCE = str_sequence("_auto_user_{0}")


def create_user(username: str = Auto, is_superuser: bool = Auto, is_staff: bool = Auto):
    username = username or next(USERNAME_SEQUENCE)
    if is_superuser is Auto:
        is_superuser = False
    if is_staff is Auto:
        is_staff = is_superuser

    return User.objects.create(username=username, is_superuser=is_superuser, is_staff=is_staff)
