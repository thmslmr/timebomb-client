from unittest.mock import patch, Mock

import tests
from timebomb.forms import WaitingForm


@patch.object(WaitingForm, "__init__", return_value=None)
def test_WaitingForm_on_ok(initpatch):
    form = WaitingForm()
    form.parentApp = Mock()

    form.on_ok()
    form.parentApp.sio.start.assert_called()


@patch.object(WaitingForm, "__init__", return_value=None)
def test_WaitingForm_on_cancel(initpatch):
    form = WaitingForm()
    form.parentApp = Mock()

    form.on_cancel()
    form.parentApp.exit.assert_called()


@patch.object(WaitingForm, "__init__", return_value=None)
@patch.object(WaitingForm, "display")
def test_WaitingForm_while_waiting(displaypatch, initpatch):
    form = WaitingForm()
    form.widgets = {"text": Mock(), "players": Mock()}
    form.ok_button = Mock()

    state = tests.create_default_gamestate(nb_players=4)
    state.room.status = "WAITING"
    form.parentApp = Mock(state=state)

    form.while_waiting()

    assert "roomname" in form.widgets["text"].value
    players = form.widgets["players"].values
    assert len(players) == 4 and players == ["name0", "name1", "name2", "name3"]
    assert form.ok_button.hidden is True
    displaypatch.assert_called_once_with()

    state.room.status = "PLAYING"
    displaypatch.reset_mock()
    form.while_waiting()

    form.parentApp.switchForm.assert_called_once_with("GAME")
    assert form.ok_button.hidden is True

    state.room.status = "READY"
    form.while_waiting()

    assert form.ok_button.hidden is False
