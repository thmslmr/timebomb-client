from unittest.mock import MagicMock
from dataclasses import fields

import timebomb.models as models


def create_dataclass_mock(datacls, **kwargs) -> MagicMock:
    """Create Mock obj for dataclass with strict spec set.

    Args:
        datacls (class): The dataclass.
        **kwargs (dict): kwargs pass to configure mock object.

    Returns:
        MagicMock: The dataclass mock object.
    """
    mockobj = MagicMock(spec_set=[field.name for field in fields(datacls)])
    mockobj.configure_mock(**kwargs)
    return mockobj


def create_default_gamestate(
    nb_players: int = 4, nb_messages: int = 10, ind_me: int = 0, ind_cutter: int = 0
) -> MagicMock:
    """Create default game state.

    Args:
        nb_players (int): Number of players to create. Default 4
        nb_messages (int): Number of messages to create. Default 10
        ind_me (int): Index of player to use as `me` state.
        ind_cutter (int): Index of player to use as `cutter`.

    Returns:
        MagicMock: The default mock game state.
    """
    state = create_dataclass_mock(models.GameState)

    players = [
        create_dataclass_mock(models.Player, **{"name": f"name{i}", "id": f"id{i}"})
        for i in range(nb_players)
    ]
    state.room = create_dataclass_mock(
        models.Room, **{"name": "roomname", "id": "roomid", "players": players}
    )
    state.room.cutter = players[ind_cutter]
    state.me = players[ind_me]

    messages = [
        create_dataclass_mock(
            models.Message, **{"player_name": f"name{i}", "content": f"content{i}"}
        )
        for i in range(nb_messages)
    ]
    state.messages = messages

    notification = create_dataclass_mock(
        models.Notification, **{"content": "notif", "read": False}
    )
    state.notification = notification

    return state
