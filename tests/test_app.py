from unittest.mock import patch, Mock

import npyscreen

import timebomb.forms as forms
from timebomb.app import App


def test_App():
    app = App()

    assert app.state and app.sio
    assert app.STARTING_FORM == "LOGIN"


@patch.object(App, "addForm")
def test_App_onStart(addpatch):
    app = App()
    app.onStart()

    addpatch.assert_any_call("LOGIN", forms.LoginForm)
    addpatch.assert_any_call("WAIT", forms.WaitingForm)
    addpatch.assert_any_call("GAME", forms.GameForm)
    addpatch.assert_any_call("NOTIF", forms.NotifForm)
    addpatch.assert_any_call("END", forms.EndForm)
    addpatch.assert_any_call("CUT", forms.CutForm)


@patch.object(npyscreen, "blank_terminal")
@patch.object(App, "switchForm")
def test_App_restart(switchpatch, blankpatch):
    app = App()
    assert app.state.room is None
    app.state.room = "TEST"
    assert app.state.room is not None

    app.restart()
    assert app.state.room is None
    blankpatch.assert_called()
    switchpatch.assert_called_once_with("LOGIN")


@patch.object(App, "switchForm")
def test_App_process_notification(switchpatch):
    app = App()
    assert app.STARTING_FORM == "LOGIN"
    assert app.NEXT_ACTIVE_FORM == "LOGIN"
    assert app.state.notification is None

    app.process_notification()
    switchpatch.assert_not_called()

    app.state.notification = Mock(read=True)

    app.process_notification()
    switchpatch.assert_not_called()

    app.state.notification = Mock(read=False)
    app.NEXT_ACTIVE_FORM = "NOTIF"
    app.process_notification()
    switchpatch.assert_not_called()

    app.state.notification = Mock(read=False)
    app.NEXT_ACTIVE_FORM = "GAME"
    app.process_notification()
    switchpatch.assert_called_once_with("NOTIF")


@patch.object(App, "switchForm")
def test_App_process_end(switchpatch):
    app = App()
    assert app.STARTING_FORM == "LOGIN"
    assert app.NEXT_ACTIVE_FORM == "LOGIN"
    assert app.state.room is None

    app.process_end()
    switchpatch.assert_not_called()

    app.state.room = Mock(status="PLAYING")
    app.process_end()
    switchpatch.assert_not_called()

    app.state.room = Mock(status="ENDED")
    app.NEXT_ACTIVE_FORM = "END"
    app.process_end()
    switchpatch.assert_not_called()

    app.state.room = Mock(status="ENDED")
    app.NEXT_ACTIVE_FORM = "NOTIF"
    app.process_end()
    switchpatch.assert_not_called()

    app.NEXT_ACTIVE_FORM = "GAME"
    app.process_end()
    switchpatch.assert_called_once_with("END")
