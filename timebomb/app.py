import sys
import npyscreen
import socketio

from timebomb.client import SocketClient
import timebomb.forms as forms


class App(npyscreen.NPSAppManaged):
    STARTING_FORM = "LOGIN"

    def __init__(self, host, *args, **kwargs):
        self.sio = SocketClient(reconnection_attempts=3, reconnection_delay=0.5)

        try:
            self.sio.connect(host)
        except socketio.exceptions.ConnectionError:
            print(f"Unable to connect to host {host}")
            sys.exit(1)

        self.state = self.sio.state
        super().__init__(*args, **kwargs)

    def onStart(self):
        self.login_form = self.addForm("LOGIN", forms.LoginForm)
        self.room_form = self.addForm("WAIT", forms.WaitingForm)
        self.main_form = self.addForm("GAME", forms.GameForm)
        self.main_form = self.addForm("NOTIF", forms.NotifForm)
        self.main_form = self.addForm("END", forms.EndForm)
        self.cut_form = self.addForm("CUT", forms.CutForm)

    def restart(self):
        npyscreen.blank_terminal()
        self.sio.init_state()

    def while_waiting(self):
        self.process_notification()
        self.process_end()

    def process_notification(self):
        if self.NEXT_ACTIVE_FORM != "NOTIF" and self.state["notification"]:
            self.switchForm("NOTIF")

    def process_end(self):
        if (
            self.NEXT_ACTIVE_FORM != "END"
            and self.state["end"]
            and self.NEXT_ACTIVE_FORM != "NOTIF"
        ):
            self.switchForm("END")

    def exit(self):
        self.sio.disconnect()
        sys.exit(1)
