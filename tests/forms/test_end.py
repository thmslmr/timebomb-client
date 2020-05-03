from unittest.mock import patch, Mock

import tests
from timebomb.forms import EndForm


@patch.object(EndForm, "__init__", return_value=None)
def test_EndForm_on_ok(initpatch):
    form = EndForm()
    form.parentApp = Mock()

    form.on_ok()
    form.parentApp.exit.assert_called()


@patch.object(EndForm, "__init__", return_value=None)
def test_EndForm_on_cancel(initpatch):
    form = EndForm()
    form.parentApp = Mock()

    form.on_cancel()
    form.parentApp.restart.assert_called()


@patch.object(EndForm, "__init__", return_value=None)
@patch.object(EndForm, "display")
def test_EndForm_while_waiting(displaypatch, initpatch):
    form = EndForm()
    form.widgets = {"text": Mock(), "team_moriarty": Mock(), "team_sherlock": Mock()}

    state = tests.create_default_gamestate(nb_players=4)
    for i, role in enumerate(["Moriarty", "Moriarty", "Sherlock", "Sherlock"]):
        state.room.players[i].team = role
    state.room.winning_team = None
    form.parentApp = Mock(state=state)

    form.while_waiting()

    displaypatch.assert_called_once_with()
    assert form.widgets["text"].value
    team_moriarty = form.widgets["team_moriarty"].values
    team_sherlock = form.widgets["team_sherlock"].values
    assert len(team_moriarty) == 2 and team_moriarty == ["name0", "name1"]
    assert len(team_sherlock) == 2 and team_sherlock == ["name2", "name3"]

    state.room.winning_team = ("Reason", "Moriarty")
    state.room.players[3].team = "Moriarty"
    displaypatch.reset_mock()
    form.while_waiting()

    displaypatch.assert_called_once_with()
    assert (
        "Reason" in form.widgets["text"].value
        and "Moriarty" in form.widgets["text"].value
    )
    team_moriarty = form.widgets["team_moriarty"].values
    team_sherlock = form.widgets["team_sherlock"].values
    assert len(team_moriarty) == 3 and team_moriarty == ["name0", "name1", "name3"]
    assert len(team_sherlock) == 1 and team_sherlock == ["name2"]
