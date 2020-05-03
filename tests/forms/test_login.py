from unittest.mock import patch, Mock

import tests
from timebomb.forms import LoginForm


@patch.object(LoginForm, "__init__", return_value=None)
def test_LoginForm_on_ok(initpatch):
    form = LoginForm()
    form.parentApp = Mock()
    form.widgets = {"username": Mock(), "roomname": Mock()}

    form.widgets["username"].value = ""
    form.widgets["roomname"].value = ""

    form.on_ok()
    form.parentApp.sio.login.assert_not_called()

    form.widgets["username"].value = "name"
    form.on_ok()
    form.parentApp.sio.login.assert_called_once_with("name", "")

    form.widgets["roomname"].value = "room"
    form.on_ok()
    form.parentApp.sio.login.assert_called_with("name", "room")


@patch.object(LoginForm, "__init__", return_value=None)
def test_LoginForm_on_cancel(initpatch):
    form = LoginForm()
    form.parentApp = Mock()

    form.on_cancel()
    form.parentApp.exit.assert_called()


@patch.object(LoginForm, "__init__", return_value=None)
def test_LoginForm_while_waiting(initpatch):
    form = LoginForm()
    state = tests.create_default_gamestate()
    form.parentApp = Mock(state=state)

    form.while_waiting()
    form.parentApp.switchForm.assert_called_once_with("WAIT")

    state.room = None
    form.parentApp.switchForm.reset_mock()
    form.while_waiting()
    form.parentApp.switchForm.assert_not_called()
