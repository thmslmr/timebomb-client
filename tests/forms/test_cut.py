from unittest.mock import patch, Mock

import tests
from timebomb.forms import CutForm


@patch.object(CutForm, "__init__", return_value=None)
def test_CutForm_while_waiting(initpatch):
    form = CutForm()
    state = tests.create_default_gamestate(nb_players=1)
    form.widgets = {"players": Mock(values=[])}
    form.get_targets = Mock(return_value=state.room.players)

    form.while_waiting()

    form.get_targets.assert_not_called()
    form.widgets["players"].update.assert_not_called()

    form.widgets = {"players": Mock(values=None)}
    form.while_waiting()

    form.get_targets.assert_called()
    form.widgets["players"].update.assert_called()

    values = form.widgets["players"].values
    assert len(values) == 1 and values[0] == "name0"


@patch.object(CutForm, "__init__", return_value=None)
def test_CutForm_get_targets(initpatch):
    form = CutForm()

    state = tests.create_default_gamestate(nb_players=3, ind_me=1)
    form.parentApp = Mock(state=state)

    targets = form.get_targets()

    assert (
        len(targets) == 2
        and targets[0] == state.room.players[0]
        and targets[1] == state.room.players[2]
    )


@patch.object(CutForm, "__init__", return_value=None)
def test_CutForm_on_ok(self):
    form = CutForm()
    form.parentApp = Mock()
    form.widgets = {"players": Mock(value=[])}

    state = tests.create_default_gamestate(nb_players=2)
    form.get_targets = Mock(return_value=state.room.players)

    form.on_ok()

    form.parentApp.sio.cut.assert_not_called()
    form.parentApp.switchForm.assert_not_called()

    form.widgets = {"players": Mock(value=[1])}
    form.on_ok()

    form.parentApp.sio.cut.assert_called_once_with("id1")
    form.parentApp.switchForm.assert_called_once_with("GAME")


@patch.object(CutForm, "__init__", return_value=None)
def test_CutForm_on_cancel(self):
    form = CutForm()
    form.parentApp = Mock()

    form.on_cancel()
    form.parentApp.switchForm.assert_called_once_with("GAME")
