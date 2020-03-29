import npyscreen
import curses

import timebomb.forms.utils as utils


class MultiLineBox(npyscreen.BoxTitle):
    _contained_widget = npyscreen.MultiLineEdit


class InputBox(npyscreen.BoxTitle):
    _contained_widget = npyscreen.Textfield


class GameForm(npyscreen.ActionFormMinimal):
    OK_BUTTON_TEXT = "QUIT"

    def create(self):
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
        message = self.widgets["input"].value.strip()
        if not message:
            return

        self.parentApp.sio.send_message(message)

        self.widgets["input"].value = ""
        self.widgets["input"].update()

    def cut_pressed(self):
        me_state = self.parentApp.state["me"]
        room_state = self.parentApp.state["room"]

        if room_state["cutter"].get("id") == me_state.get("id"):
            self.parentApp.switchForm("CUT")

    def while_waiting(self):
        self.process_chat_message()
        self.process_room_state()
        self.process_player_state()
        self.display()

    def process_room_state(self):
        room_state = self.parentApp.state["room"]
        players = room_state.get("players", [])

        player_names = []
        for player in players:
            if room_state["cutter"]["id"] == player["id"]:
                player_names.append(player["name"] + " [cut]")
            else:
                player_names.append(player["name"])

        self.widgets["players"].name = f"Players [{len(players)}]"
        self.widgets["players"].values = player_names

        self.widgets["cards_found"].value = utils.summary_deck(
            room_state.get("cards_found")
        )
        self.widgets["cards_left"].value = utils.summary_deck(
            room_state.get("cards_left")
        )

        nb_found = sum(room_state.get("cards_found", {}).values())
        nb_left = sum(room_state.get("cards_left", {}).values())

        complete_str = (
            "│"
            + ("█" * len(players) + "│") * (nb_found // len(players))
            + "█" * (nb_found % len(players))
        )
        left_str = (
            "░" * (nb_left % len(players))
            + ("│" if nb_left % len(players) else "")
            + ("░" * len(players) + "│") * (nb_left // len(players))
        )

        self.widgets["round"].value = complete_str + left_str

    def process_player_state(self):
        me_state = self.parentApp.state["me"]
        room_state = self.parentApp.state["room"]

        self.widgets["cards_user"].value = utils.list_deck(me_state.get("hand"))

        color = "DANGER" if me_state.get("team") == "Moriarty" else "NO_EDIT"

        self.color = color
        self.widgets["cut"].hidden = room_state["cutter"].get("id") != me_state.get(
            "id"
        )

        for widget in self.widgets.values():
            widget.color = color
            widget.labelColor = color

        self.name = f"Time Bomb ── {me_state['name']} ── Team {me_state['team']}"

    def process_chat_message(self):
        messages = self.parentApp.state["messages"]

        if not messages:
            return

        max_message = self.widgets["message"].height - 2
        self.widgets["message"].value = "\n".join(
            [
                message["player"] + ":\t" + message["message"]
                for message in messages[-max_message:]
            ]
        )

    def on_ok(self):
        self.parentApp.exit()
