import npyscreen


class WaitingForm(npyscreen.ActionForm):
    """Form between login and start of the game."""

    CANCEL_BUTTON_BR_OFFSET = (2, 14)
    OK_BUTTON_TEXT = "START"
    CANCEL_BUTTON_TEXT = "LOGOUT"

    DEFAULT_LINES = 18
    DEFAULT_COLUMNS = 72

    def create(self):
        """Create widgets."""
        self.keypress_timeout = 1
        self.name = "Time bomb"
        self.center_on_display()

        self.widgets = {
            "text": self.add(npyscreen.MultiLineEdit, editable=False, height=2),
            "players": self.add(
                npyscreen.TitleMultiLine,
                name="Players :",
                editable=False,
                rely=self.nextrely + 1,
            ),
        }

    def while_waiting(self):
        """Update form or switch to game is playing."""
        state = self.parentApp.state.room
        players = state.players

        if state.status == "PLAYING":
            self.parentApp.switchForm("GAME")

        text = (
            f"You have entered room: {state.name}.\n"
            + "Need at least 4 players to start the game."
        )
        self.widgets["text"].value = text
        self.widgets["players"].values = [player.name for player in players]

        self.ok_button.hidden = state.status != "READY"

        self.display()

    def on_ok(self):
        """Emit start message."""
        self.parentApp.sio.start()

    def on_cancel(self):
        """Exit game."""
        self.parentApp.exit()
