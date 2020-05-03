from unittest.mock import patch, Mock

import tests
from timebomb.forms import GameForm


@patch.object(GameForm, "__init__", return_value=None)
def test_GameForm_send_message(initpatch):
    form = GameForm()
    form.parentApp = Mock()
    form.widgets = {"input": Mock()}

    form.widgets["input"].value = " "
    form.send_message(None)

    form.parentApp.sio.send_message.assert_not_called()
    assert form.widgets["input"].value == " "
    form.widgets["input"].update.assert_not_called()

    form.widgets["input"].value = "message "
    form.send_message(None)

    form.parentApp.sio.send_message.assert_called_once_with("message")
    assert form.widgets["input"].value == ""
    form.widgets["input"].update.assert_called()


@patch.object(GameForm, "__init__", return_value=None)
def test_GameForm_cut_pressed(initpatch):
    form = GameForm()

    state = tests.create_default_gamestate(nb_players=4, ind_me=1, ind_cutter=0)
    form.parentApp = Mock(state=state)

    form.cut_pressed()
    form.parentApp.switchForm.assert_not_called()

    state.room.cutter.id = "id1"
    form.cut_pressed()
    form.parentApp.switchForm.assert_called_once_with("CUT")


@patch.object(GameForm, "__init__", return_value=None)
def test_GameForm_on_ok(initpatch):
    form = GameForm()
    form.parentApp = Mock()

    form.on_ok()
    form.parentApp.exit.assert_called()


@patch.object(GameForm, "__init__", return_value=None)
def test_GameForm_process_chat_message(initpatch):
    form = GameForm()

    form.widgets = {"message": Mock()}
    form.widgets["message"].value = None
    form.widgets["message"].height = 100

    state = tests.create_default_gamestate(nb_messages=0)
    form.parentApp = Mock(state=state)

    form.process_chat_message()

    assert form.widgets["message"].value is None

    state = tests.create_default_gamestate(nb_messages=4)
    form.parentApp.state = state

    form.process_chat_message()
    messages = form.widgets["message"].value.split("\n")
    assert len(messages) == 4

    form.widgets["message"].height = 4
    form.process_chat_message()
    messages = form.widgets["message"].value.split("\n")
    assert len(messages) == 2


@patch.object(GameForm, "__init__", return_value=None)
@patch("timebomb.forms.utils.list_deck", return_value="deck")
def test_GameForm_process_player_state(utilspatch, initpatch):
    form = GameForm()
    form.widgets = {"cards_user": Mock(), "cut": Mock()}

    state = tests.create_default_gamestate(nb_players=4, ind_me=2, ind_cutter=1)
    state.me.team = "Moriarty"
    state.me.hand = ["A", "B", "C"]
    form.parentApp = Mock(state=state)

    form.process_player_state()

    utilspatch.assert_called_once_with(["A", "B", "C"])
    assert form.widgets["cards_user"].value == "deck"
    assert form.color == "DANGER"
    assert form.widgets["cut"].hidden is True
    assert form.name == "Time Bomb ── name2 ── Team Moriarty"

    state.me.team = "Sherlock"
    utilspatch.reset_mock()
    form.process_player_state()

    utilspatch.assert_called_once_with(["A", "B", "C"])
    assert form.color == "NO_EDIT"
    assert form.name == "Time Bomb ── name2 ── Team Sherlock"

    state.room.cutter.id = "id2"
    form.process_player_state()
    assert form.widgets["cut"].hidden is False


@patch.object(GameForm, "__init__", return_value=None)
@patch("timebomb.forms.game.utils")
def test_GameForm_process_room_state(utilspatch, initpatch):
    form = GameForm()
    form.widgets = {
        k: Mock() for k in ["players", "cards_found", "cards_left", "round"]
    }

    state = tests.create_default_gamestate(nb_players=4, ind_cutter=1)
    state.room.cards_found = {"A": 10}
    state.room.cards_left = {"B": 10}

    form.parentApp = Mock(state=state)

    utilspatch.summary_deck = lambda x: str(x)
    utilspatch.round_bar = lambda *x: str(x)

    form.process_room_state()

    assert form.widgets["players"].name == "Players [4]"
    assert form.widgets["players"].values == ["name0", "name1 [cut]", "name2", "name3"]

    assert form.widgets["cards_found"].value == "{'A': 10}"
    assert form.widgets["cards_left"].value == "{'B': 10}"
    assert form.widgets["round"].value == "(4, 10, 10)"
