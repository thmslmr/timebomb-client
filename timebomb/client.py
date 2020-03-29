import socketio
import copy

INIT_STATE = {"messages": [], "room": {}, "me": {}, "notification": {}, "end": {}}


class SocketClient(socketio.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.state = copy.deepcopy(INIT_STATE)

        self.on("chat", self.chat_handler)
        self.on("room", self.room_handler)
        self.on("player", self.player_handler)
        self.on("end", self.end_handler)
        self.on("notify", self.notif_handler)

    def chat_handler(self, data):
        self.state["messages"].append(data)
        self.state["messages"] = self.state["messages"][-100:]

    def room_handler(self, data):
        self.state["room"].update(data)

    def player_handler(self, data):
        self.state["me"].update(data)

    def end_handler(self, data):
        self.state["end"] = data

    def notif_handler(self, data):
        self.state["notification"] = data

    def init_state(self):
        self.state.update(INIT_STATE)

    def login(self, username, roomname):
        self.emit("login", {"username": username, "roomname": roomname})

    def start(self):
        self.emit("start")

    def cut(self, target_id):
        self.emit("cut", {"target": target_id})

    def send_message(self, message):
        self.emit("chat", {"message": message})
