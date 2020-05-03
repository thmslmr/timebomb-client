from unittest.mock import patch, Mock

from timebomb.client import SocketClient


def test_Client():
    statemock = Mock()
    client = SocketClient(state=statemock)

    handlers = client.handlers["/"]
    assert handlers["chat"] == statemock.new_message
    assert handlers["room"] == statemock.update_room
    assert handlers["player"] == statemock.update_me
    assert handlers["notify"] == statemock.new_notification

    # Test fix support end status.
    client.handlers["/"]["end"]({"data": "value"})
    statemock.update_room.assert_called_once_with({"data": "value", "status": "ENDED"})


@patch.object(SocketClient, "emit")
def test_Client_emits(emitpatch):
    client = SocketClient(Mock())

    client.login("player", "room")
    data = {"username": "player", "roomname": "room"}
    emitpatch.assert_called_with("login", data)

    client.start()
    emitpatch.assert_called_with("start")

    client.cut("tid")
    emitpatch.assert_called_with("cut", {"target": "tid"})

    client.send_message("mymessage")
    emitpatch.assert_called_with("chat", {"message": "mymessage"})
