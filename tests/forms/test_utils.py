import timebomb.forms.utils as utils


def test_card_view():
    value = "A"
    view = utils.card_view(value)

    assert view == "┌───┐\n│ A │\n└───┘"


def test_summary_deck():
    deck = {}
    view = utils.summary_deck(deck)

    assert view == ""

    deck = {"A": 4}
    view = utils.summary_deck(deck)
    expected_view = "┌───┐    \n│ A │ x4 \n└───┘    \n"
    assert view == expected_view

    deck = {"A": 4, "B": 5}
    view = utils.summary_deck(deck)
    expected_view = "┌───┐     ┌───┐    \n│ A │ x4  │ B │ x5 \n└───┘     └───┘    \n"
    assert view == expected_view


def test_list_deck():
    deck = {}
    view = utils.list_deck(deck)

    assert view == ""

    deck = ["A"]
    view = utils.list_deck(deck)

    assert view == "┌───┐\n│ A │\n└───┘\n"

    deck = ["A", "B"]
    view = utils.list_deck(deck)

    assert view == "┌───┐ ┌───┐\n│ A │ │ B │\n└───┘ └───┘\n"


def test_round_bar():
    view = utils.round_bar(4, 0, 20)
    assert view == "│░░░░│░░░░│░░░░│░░░░│░░░░│"

    view = utils.round_bar(5, 0, 25)
    assert view == "│░░░░░│░░░░░│░░░░░│░░░░░│░░░░░│"

    view = utils.round_bar(4, 1, 19)
    assert view == "│█░░░│░░░░│░░░░│░░░░│░░░░│"

    view = utils.round_bar(4, 5, 15)
    assert view == "│████│█░░░│░░░░│░░░░│░░░░│"

    view = utils.round_bar(4, 10, 10)
    assert view == "│████│████│██░░│░░░░│░░░░│"

    view = utils.round_bar(4, 20, 0)
    assert view == "│████│████│████│████│████│"
