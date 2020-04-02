Time Bomb Client
---
[![pypi](https://img.shields.io/pypi/v/timebomb-client.svg)](https://pypi.python.org/pypi/timebomb-client)
[![versions](https://img.shields.io/pypi/pyversions/timebomb-client.svg)](https://github.com/thmslmr/timebomb-client)

**UNDER DEVELOPMENT**

Just enough to connect a [timebomb-server](https://github.com/thmslmr/timebomb-server) and play Time Bomb in your terminal.

Dependencies
---

`timebomb-client` supports Python 3.6+.

Installation requires [python-socketio](https://github.com/miguelgrinberg/python-socketio) and [npyscreen](https://github.com/npcole/npyscreen).

Installation
---

Install the latest stable release from PyPI:

```bash
$ pip install timebomb-client --user
```

Run
---

Connect to a specific `timebomb-server` and start playing.

```bash
$ timebomb HOST.ADDRESS
```

Rules
---

If you're not familiar with this game and want to know more about the rules, check out the [The *almost*-Official Rulebook](./RULES.md).

Disclaimer: As this is a terminal implementation, the game is not strictly following those rules, some parts are automated (card shuffling, dealing, random picking, etc...).

License
---

This project is under [MIT License](./LICENSE).
