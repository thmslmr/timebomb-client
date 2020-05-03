from unittest.mock import patch, Mock

import tests
from timebomb.forms import NotifForm


@patch.object(NotifForm, "__init__", return_value=None)
def test_NotifForm_on_ok(initpatch):
    form = NotifForm()
    state = tests.create_default_gamestate()
    form.parentApp = Mock(state=state)
    assert not state.notification.read

    form.on_ok()
    assert state.notification.read
    form.parentApp.setNextFormPrevious.assert_called_once_with()


@patch.object(NotifForm, "__init__", return_value=None)
def test_NotifForm_while_waiting(initpatch):
    form = NotifForm()
    form.text = Mock()

    state = tests.create_default_gamestate()
    form.parentApp = Mock(state=state)
    assert state.notification.content == "notif"

    form.while_waiting()
    assert form.text.value == "notif"
    form.text.update.assert_called_once_with()
