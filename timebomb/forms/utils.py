def card_view(value: str) -> str:
    return "┌───┐\n│ {} │\n└───┘".format(value)


def summary_deck(deck: dict) -> str:
    if not deck:
        return ""
    lines = [card_view(card).split("\n") for card in deck.keys()]

    for i, (k, v) in enumerate(deck.items()):
        lines.insert(1 + (i * 2), ["   ", "x{} ".format(v), "   "])

    output = ""

    for line in zip(*lines):
        output += " ".join(line) + "\n"

    return output


def list_deck(deck: list) -> str:
    if not deck:
        return ""
    lines = [card_view(card).split("\n") for card in deck]
    output = ""

    for line in zip(*lines):
        output += " ".join(line) + "\n"

    return output
