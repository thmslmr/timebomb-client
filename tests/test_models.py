from datetime import datetime

import timebomb.models as models


def test_Notification():
    notif = models.Notification("message")

    assert notif.content == "message"
    assert notif.read is False
    assert str(notif) == "message"


def test_Player():
    player = models.Player("name", "id")

    assert player.name == "name"
    assert player.id == "id"
    assert player.team is None
    assert player.hand is None

    player = models.Player("name", "id", "team", ("A", "B"), "roomid")

    assert player.name == "name"
    assert player.id == "id"
    assert player.team == "team"
    assert player.hand == ("A", "B")
    assert player.roomId == "roomid"


def test_Message():
    now = datetime.now()
    message = models.Message("player", "message")

    assert message.player_name == "player"
    assert message.content == "message"
    assert message.timestamp and isinstance(message.timestamp, datetime)
    assert str(message) == f"[{now:%H:%M}] player: message"


def test_Room():
    player = models.Player("player", "player_id")
    room = models.Room("room", "room_id", (player,))

    assert room.name == "room" and room.id == "room_id"
    assert len(room.players) == 1 and room.players[0] is player

    assert room.cutter is None and room.winning_team is None and room.status == ""

    assert isinstance(room.cards_found, dict) and isinstance(room.cards_left, dict)
    assert not room.cards_found and not room.cards_left


def test_GameState():
    state = models.GameState()

    assert isinstance(state.messages, list) and not state.messages
    assert state.room is None and state.me is None and state.notification is None


def test_GameState_new_message():
    state = models.GameState()

    assert isinstance(state.messages, list) and not state.messages

    message = state.new_message({"player": "player", "message": "test_message"})

    assert len(state.messages) == 1 and state.messages[0] is message
    assert message.player_name == "player" and message.content == "test_message"

    for i in range(99):
        last = state.new_message(
            {"player": f"player{i}", "message": f"test_message{i}"}
        )

    assert len(state.messages) == 100
    assert state.messages[0] is message and state.messages[99] is last
    assert last.player_name == "player98" and last.content == "test_message98"

    last = state.new_message({"player": "player99", "message": "test_message99"})

    assert len(state.messages) == 100
    assert state.messages[0] is not message and state.messages[99] is last
    assert (
        state.messages[0].player_name == "player0"
        and state.messages[0].content == "test_message0"
    )
    assert last.player_name == "player99" and last.content == "test_message99"

    res = state.new_message({"message": "test_message100"})

    assert res is None
    assert state.messages[99] is last


def test_GameState_new_notification():
    state = models.GameState()
    assert state.notification is None

    notif1 = state.new_notification({"message": "notif1"})
    assert state.notification is notif1 and notif1.content == "notif1"

    notif2 = state.new_notification({"message": "notif2"})
    assert state.notification is notif2 and notif2.content == "notif2"

    notif3 = state.new_notification({"unknown": "notif2"})
    assert notif3 is None and state.notification is notif2


def test_GameState_update_room():
    state = models.GameState()
    assert state.room is None

    players_data = [{"name": "player1", "id": "id1"}]
    room_data = {"name": "roomname", "id": "roomid", "players": players_data}
    room = state.update_room(room_data)

    assert state.room is room and room.name == "roomname" and room.id == "roomid"
    assert len(room.players) == 1
    assert room.players[0].name == "player1" and room.players[0].id == "id1"

    new_data = {"name": "newname", "cutter": {"name": "cutter", "id": "cutterid"}}
    room = state.update_room(new_data)

    assert state.room is room and room.name == "newname" and room.id == "roomid"
    assert len(room.players) == 1
    assert room.players[0].name == "player1" and room.players[0].id == "id1"
    assert (
        isinstance(room.cutter, models.Player)
        and room.cutter.id == "cutterid"
        and room.cutter.name == "cutter"
    )

    new_data = {
        "players": [{"name": "player1", "id": "id1"}, {"name": "player2", "id": "id2"}]
    }
    room = state.update_room(new_data)

    assert state.room is room and room.name == "newname" and room.id == "roomid"
    assert len(room.players) == 2


def test_GameState_update_me():
    state = models.GameState()
    assert state.me is None

    player = state.update_me({"name": "player1", "id": "id1"})
    assert state.me is player and player.name == "player1" and player.id == "id1"
    assert player.hand is None

    player = state.update_me({"hand": ("A", "A", "B", "A")})
    assert state.me is player and player.name == "player1" and player.id == "id1"
    assert player.hand == ("A", "A", "B", "A")


def test_GameState_reset():
    state = models.GameState()

    assert isinstance(state.messages, list) and not state.messages
    assert state.room is None and state.me is None and state.notification is None

    state.messages = ["m1", "m2"]
    state.room = "Room"
    state.me = "Me"
    state.notification = "Notification"

    state.reset()
    assert isinstance(state.messages, list) and not state.messages
    assert state.room is None and state.me is None and state.notification is None
