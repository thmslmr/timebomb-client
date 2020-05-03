import npyscreen


class CutForm(npyscreen.ActionForm):
    """Form display when user want to cut a card."""

    CANCEL_BUTTON_TEXT = "CANCEL"
    OK_BUTTON_TEXT = "CUT"

    DEFAULT_COLUMNS = 60
    DEFAULT_LINES = 12

    def create(self):
        """Create Form."""
        self.keypress_timeout = 1
        self.center_on_display()

        self.name = "Who to cut ?"
        self.widgets = {
            "players": self.add(
                npyscreen.TitleSelectOne,
                scroll_exit=True,
                name="Players",
                values=range(7),
            )
        }
        # HACK
        self.widgets["players"].entry_widget.cursor_line = 0

    def while_waiting(self):
        """Use to display properly player names."""
        if type(self.widgets["players"].values) is not list:
            targets = self.get_targets()
            self.widgets["players"].values = [t.name for t in targets]
            self.widgets["players"].update()

    def get_targets(self):
        """Get list of sorted (by name) potential targets.

        Returns:
            list: List of player objects.
        """
        room_state = self.parentApp.state.room
        me_state = self.parentApp.state.me
        return sorted(
            [player for player in room_state.players if player.id != me_state.id],
            key=lambda item: item.name,
        )

    def on_ok(self):
        """Emit cut event and switch form once ok is hit."""
        value = self.widgets["players"].value
        if len(value) == 0:
            return

        targets = self.get_targets()
        target_id = [t.id for t in targets][value[0]]

        self.parentApp.sio.cut(target_id)
        self.parentApp.switchForm("GAME")

    def on_cancel(self):
        """Back to game form."""
        self.parentApp.switchForm("GAME")
