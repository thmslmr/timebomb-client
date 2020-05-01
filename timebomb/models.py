import dataclasses
from datetime import datetime
from typing import List, Tuple, Dict


@dataclasses.dataclass
class Notification:
    """Hold Notification data."""

    content: str
    read: bool = dataclasses.field(default=False, init=False)

    def __str__(self):
        return self.content


@dataclasses.dataclass(frozen=True)
class Player:
    """Hold player data."""

    name: str
    id: str
    team: str = None
    hand: Tuple[str] = None


@dataclasses.dataclass(frozen=True)
class Message:
    """Hold chat message data."""

    player_name: str
    content: str
    timestamp: datetime = dataclasses.field(default_factory=datetime.now)

    def __str__(self):
        return f"[{self.timestamp:%H:%M}] {self.player_name}: {self.content}"


@dataclasses.dataclass(frozen=True)
class Room:
    """Hold room data."""

    name: str
    id: str
    players: Tuple[Player]

    cutter: str = ""
    status: str = ""
    winning_team: Tuple[str] = None

    cards_found: Dict[str, int] = dataclasses.field(default_factory=dict)
    cards_left: Dict[str, int] = dataclasses.field(default_factory=dict)


@dataclasses.dataclass
class GameState:
    """Hold overall game state."""

    messages: List[Message] = dataclasses.field(default_factory=list)
    room: Room = None
    me: Player = None
    notification: Notification = None

    def new_message(self, data: dict) -> Message:
        """Add new message in messages list.

        Args:
            data (dict): Dict containing message data.

        Returns:
            Message: Newly created message.
        """
        player_name = data.get("player")
        content = data.get("message")

        if not player_name or not content:
            return  # TODO: Warning

        message = Message(player_name, content)
        self.messages.append(message)
        self.messages = self.messages[-100:]
        return message

    def new_notification(self, data: dict) -> Notification:
        """Create new notification object.

        Args:
            data (dict): Dict containing notification data.

        Returns:
            Notification: Newly created notification.
        """
        message = data.get("message")

        if not message:
            return  # TODO: Warning

        notification = Notification(message)
        self.notification = notification
        return notification

    def update_room(self, data: dict) -> Room:
        """Create or update room attribute.

        Args:
            data (dict): Dict containing room data.

        Returns:
            Room: Newly created room.
        """
        # Separate treatment for players
        players_infos = data.pop("players", [])
        if players_infos:
            players = [Player(**infos) for infos in players_infos]
            data["players"] = players

        if self.room is None:
            new_room = Room(**data)
        else:
            new_room = dataclasses.replace(self.room, **data)

        self.room = new_room
        return new_room

    def update_me(self, data: dict) -> Player:
        """Create or update me attribute.

        Args:
            data (dict): Dict containg player data.

        Returns:
            Player: Newly created player.
        """
        if self.me is None:
            new_me = Player(**data)
        else:
            new_me = dataclasses.replace(self.me, **data)

        self.me = new_me
        return new_me
