import sys
import npyscreen
import socketio

from timebomb.client import SocketClient
from timebomb.models import GameState
import timebomb.forms as forms


class App(npyscreen.NPSAppManaged):
    """Time Bomb App."""

    STARTING_FORM = "LOGIN"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.state = GameState()
        self.sio = SocketClient(
            self.state, reconnection_attempts=3, reconnection_delay=0.5
        )

    def connect_server(self, host: str):
        """Connect to socket io server.

        Args:
            host (str): Host to connect to.
        """
        try:
            self.sio.connect(host)
        except socketio.exceptions.ConnectionError:
            print(f"Unable to connect to host {host}")
            sys.exit(1)

    def onStart(self):
        """Add all forms."""
        self.addForm("LOGIN", forms.LoginForm)
        self.addForm("WAIT", forms.WaitingForm)
        self.addForm("GAME", forms.GameForm)
        self.addForm("NOTIF", forms.NotifForm)
        self.addForm("END", forms.EndForm)
        self.addForm("CUT", forms.CutForm)

    def restart(self):
        """Clear terminal and reset game state."""
        npyscreen.blank_terminal()
        self.state.reset()
        self.switchForm("LOGIN")

    def while_waiting(self):
        """Process notification then end event."""
        self.process_notification()
        self.process_end()

    def process_notification(self):
        """Display notification form if unread notif."""
        if (
            self.NEXT_ACTIVE_FORM != "NOTIF"
            and self.state.notification
            and not self.state.notification.read
        ):
            self.switchForm("NOTIF")

    def process_end(self):
        """Display end form if winning team in room state."""
        if (
            self.NEXT_ACTIVE_FORM != "END"
            and self.NEXT_ACTIVE_FORM != "NOTIF"
            and self.state.room
            and self.state.room.status == "ENDED"
        ):
            self.switchForm("END")

    def exit(self):
        """Disconnect from server and exit."""
        self.sio.disconnect()
        sys.exit(0)
