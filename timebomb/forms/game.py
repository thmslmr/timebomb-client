import npyscreen
import curses

import timebomb.forms.utils as utils


class MultiLineBox(npyscreen.BoxTitle):
    _contained_widget = npyscreen.MultiLineEdit


class InputBox(npyscreen.BoxTitle):
    _contained_widget = npyscreen.Textfield


class GameForm(npyscreen.ActionFormMinimal):
    """Main form used during game."""

    OK_BUTTON_TEXT = "QUIT"

    def create(self):
        """Create widgets."""
        self.keypress_timeout = 1
        self.name = "Time Bomb"

        height, width = self.useable_space()
        new_handlers = {curses.ascii.alt(curses.ascii.NL): self.send_message}
        self.add_handlers(new_handlers)
        self.widgets = {
            "round": self.add(
                npyscreen.TitleFixedText,
                name="Round",
                value="salut",
                editable=False,
                use_two_lines=False,
                width=width - 20,
            ),
            "cut": self.add(
                npyscreen.ButtonPress,
                name="CUT",
                when_pressed_function=self.cut_pressed,
                relx=width - 10,
                rely=2,
                width=5,
                height=1,
                hidden=True,
            ),
            "players": self.add(
                npyscreen.TitleMultiLine,
                scroll_exit=True,
                name="Players",
                values=[],
                rely=self.nextrely + 1,
                width=width // 2 - 1,
                height=4,
            ),
            "cards_found": self.add(
                MultiLineBox,
                name="Cards found",
                editable=False,
                rely=self.nextrely + 1,
                height=5,
                max_width=width // 2 - 2,
                value="ca va ?",
            ),
            "cards_left": self.add(
                MultiLineBox,
                name="Cards left",
                editable=False,
                height=5,
                max_width=width // 2 - 2,
                value="laklak",
            ),
            "cards_user": self.add(
                MultiLineBox,
                name="Your cards",
                editable=False,
                height=5,
                max_width=width // 2 - 2,
                value="et toi ?",
            ),
            "message": self.add(
                MultiLineBox,
                name="Messages",
                editable=False,
                rely=4,
                relx=width // 2 + 1,
                width=width // 2 - 1,
                height=height - 9,
            ),
            "input": self.add(
                InputBox,
                name="Write (alt+ENTER)",
                relx=width // 2 + 1,
                rely=height - 5,
                height=3,
                width=width // 2 - 1,
            ),
        }

    def send_message(self, widget):
        """Send message and clear input."""
        message = self.widgets["input"].value.strip()
        if not message:
            return

        self.parentApp.sio.send_message(message)

        self.widgets["input"].value = ""
        self.widgets["input"].update()

    def cut_pressed(self):
        """Display cut form when hitting cut button."""
        me_state = self.parentApp.state.me
        room_state = self.parentApp.state.room

        if room_state.cutter.id == me_state.id:
            self.parentApp.switchForm("CUT")

    def while_waiting(self):
        """Update chat, self infos and room infos."""
        self.process_chat_message()
        self.process_room_state()
        self.process_player_state()
        self.display()

    def process_room_state(self):
        """Display players and room cards."""
        room_state = self.parentApp.state.room
        players = room_state.players

        player_names = []
        for player in players:
            if room_state.cutter.id == player.id:
                player_names.append(f"{player.name} [cut]")
            else:
                player_names.append(player.name)

        self.widgets["players"].name = f"Players [{len(players)}]"
        self.widgets["players"].values = player_names

        self.widgets["cards_found"].value = utils.summary_deck(room_state.cards_found)
        self.widgets["cards_left"].value = utils.summary_deck(room_state.cards_left)

        nb_found = sum(room_state.cards_found.values())
        nb_left = sum(room_state.cards_left.values())
        nb_players = len(players)

        self.widgets["round"].value = utils.round_bar(nb_players, nb_found, nb_left)

    def process_player_state(self):
        """Display deck and change style."""
        me_state = self.parentApp.state.me
        room_state = self.parentApp.state.room

        self.widgets["cards_user"].value = utils.list_deck(me_state.hand)

        color = "DANGER" if me_state.team == "Moriarty" else "NO_EDIT"

        self.color = color
        self.widgets["cut"].hidden = room_state.cutter.id != me_state.id

        for widget in self.widgets.values():
            widget.color = color
            widget.labelColor = color

        self.name = f"Time Bomb ── {me_state.name} ── Team {me_state.team}"

    def process_chat_message(self):
        """Display messages in chat."""
        messages = self.parentApp.state.messages

        if not messages:
            return

        max_message = self.widgets["message"].height - 2
        self.widgets["message"].value = "\n".join(
            [str(message) for message in messages[-max_message:]]
        )

    def on_ok(self):
        """Exit game."""
        self.parentApp.exit()  # TODO: add confirmation form
