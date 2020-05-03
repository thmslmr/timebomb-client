import socketio


class SocketClient(socketio.Client):
    """Socket Client to interact with timebomb server."""

    def __init__(self, state, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.on("chat", state.new_message)
        self.on("room", state.update_room)
        self.on("player", state.update_me)

        # TODO: Change server side to handle that
        self.on("end", lambda data: state.update_room({**data, "status": "ENDED"}))
        self.on("notify", state.new_notification)

    def login(self, username: str, roomname: str = None):
        """Emit socket message to login.

        Args:
            username (str): The user name.
            roomname (str): The room name. Default None.
        """
        self.emit("login", {"username": username, "roomname": roomname})

    def start(self):
        """Emit socket message to start the game."""
        self.emit("start")

    def cut(self, target_id):
        """Emit socket message to randomly cut a card.

        Args:
            target_id (str): The player id where to cut.
        """
        self.emit("cut", {"target": target_id})

    def send_message(self, message):
        """Emit socket message for chat.

        Args:
            message (str): The message to send.
        """
        self.emit("chat", {"message": message})
