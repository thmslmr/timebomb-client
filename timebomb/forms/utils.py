def card_view(value: str) -> str:
    """Create string card view.

    Args:
        value (str): Value of the card

    Returns:
        str: The card view.
    """
    return f"┌───┐\n│ {value} │\n└───┘"


def summary_deck(deck: dict) -> str:
    """Create deck summary view (used for card found / left).

    Args:
        deck (dict): Dict where key if card and value is count.

    Returns:
        str: The deck summary view.
    """
    if not deck:
        return ""

    lines = [card_view(card).split("\n") for card in deck.keys()]

    for i, (k, v) in enumerate(deck.items()):
        lines.insert(1 + (i * 2), ["   ", f"x{v} ", "   "])

    output = ""

    for line in zip(*lines):
        output += " ".join(line) + "\n"

    return output


def list_deck(deck: list) -> str:
    """Detailed view of deck card by card.

    Args:
        deck (list): List of cards value.

    Returns:
        str: The deck list view.
    """
    if not deck:
        return ""

    lines = [card_view(card).split("\n") for card in deck]
    output = ""

    for line in zip(*lines):
        output += " ".join(line) + "\n"

    return output


def round_bar(nb_players: int, nb_found: int, nb_left: int) -> str:
    """Get round progress bar.

    Args:
        nb_players (int): Number of players.
        nb_found (int): Number of cards found.
        nb_left (int): Number of cards left.

    Returns:
        str: Round progress bar.
    """
    complete_str = (
        "│"
        + ("█" * nb_players + "│") * (nb_found // nb_players)
        + "█" * (nb_found % nb_players)
    )
    left_str = (
        "░" * (nb_left % nb_players)
        + ("│" if nb_left % nb_players else "")
        + ("░" * nb_players + "│") * (nb_left // nb_players)
    )

    return complete_str + left_str
