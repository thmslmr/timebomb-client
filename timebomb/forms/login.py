import npyscreen


ACSII = r"""
  _____ _             ___            _
 |_   _(_)_ __  ___  | _ ) ___ _ __ | |__
   | | | | '  \/ -_) | _ \/ _ \ '  \| '_ \
   |_| |_|_|_|_\___| |___/\___/_|_|_|_.__/
"""

CONSIGNE = """
To start a game, chose you username (mandatory field).
You can join or create a room by entering its name (optinal field).
Otherwise, you will be added to a random room.
"""


class LoginForm(npyscreen.ActionForm):
    """Log to start a new game."""

    CANCEL_BUTTON_BR_OFFSET = (2, 14)
    OK_BUTTON_TEXT = "LOGIN"
    CANCEL_BUTTON_TEXT = "QUIT"

    DEFAULT_LINES = 18
    DEFAULT_COLUMNS = 72

    def create(self):
        """Display infos and create widgets."""
        self.name = "Welcome"
        self.keypress_timeout = 1
        self.center_on_display()

        self.add(
            npyscreen.MultiLineEdit,
            value=f"{ACSII}\n{CONSIGNE}",
            editable=False,
            height=10,
        )

        self.widgets = {
            "username": self.add(npyscreen.TitleText, name="Username *:"),
            "roomname": self.add(npyscreen.TitleText, name="Roomname:"),
        }

    def on_ok(self):
        """Login if username is defined."""
        username = self.widgets["username"].value.strip()
        if not username:
            return

        roomname = self.widgets["roomname"].value.strip()
        self.parentApp.sio.login(username, roomname)

    def on_cancel(self):
        """Exit if cancel."""
        self.parentApp.exit()

    def while_waiting(self):
        """Wait for room to exist and switch to wait form."""
        if self.parentApp.state.room:
            self.parentApp.switchForm("WAIT")
