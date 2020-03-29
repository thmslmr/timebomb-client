import itertools
import npyscreen


class EndForm(npyscreen.ActionForm):
    DEFAULT_LINES = 18
    DEFAULT_COLUMNS = 72

    CANCEL_BUTTON_BR_OFFSET = (2, 12)
    OK_BUTTON_TEXT = "QUIT"
    CANCEL_BUTTON_TEXT = "REPLAY"

    def create(self):
        self.name = "Game Over"
        self.keypress_timeout = 1
        self.center_on_display()

        self.widgets = {
            "text": self.add(npyscreen.Textfield, editable=False),
            "team_moriarty": self.add(
                npyscreen.TitleMultiLine,
                editable=False,
                height=4,
                name="Team Moriarty",
                values=[],
                labelColor="DANGER",
                rely=self.nextrely + 1,
            ),
            "team_sherlock": self.add(
                npyscreen.TitleMultiLine,
                editable=False,
                height=6,
                name="Team Sherlock",
                values=[],
                labelColor="NO_EDIT",
            ),
        }

    def on_ok(self):
        self.parentApp.exit()

    def on_cancel(self):
        self.parentApp.restart()
        self.parentApp.switchForm("LOGIN")

    def while_waiting(self):
        end_state = self.parentApp.state["end"]

        if end_state["winning_team"] is None:
            self.widgets[
                "text"
            ].value = "The game has ended due to an unexpected error. No winner."
        else:
            team, reason = end_state["winning_team"]
            text = f"{reason} Team {team} won !\n"
            self.widgets["text"].value = text

        groups = {}
        data = sorted(end_state["players"], key=lambda player: player["team"])
        for k, g in itertools.groupby(data, lambda player: player["team"]):
            groups[k] = list(g)

        moriarty_names = [player["name"] for player in groups["Moriarty"]]
        sherlock_names = [player["name"] for player in groups["Sherlock"]]

        self.widgets["team_moriarty"].values = moriarty_names
        self.widgets["team_sherlock"].values = sherlock_names

        self.display()
