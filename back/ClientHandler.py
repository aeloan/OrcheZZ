import socket
from typing import Optional, Callable

from ClientRequestDispatcher import ClientRequestDispatcher
from Room import Room
from common.BaseHandler import BaseHandler
from common.SockerFramer import SocketFramer


class ClientHandler(BaseHandler):
    def __init__(self, socket: socket.socket, address: str, manager):
        super().__init__(socket)
        self.address = address
        self.manager = manager
        self.room: Optional[Room] = None
        self.client_name = None

    def get_dispatcher(self) -> dict[str, Callable]:
        return ClientRequestDispatcher.handlers

    def close(self):
        super().close()
        self.manager.remove_client(self)
        self.leave_room()
        self.manager = None

    def set_room(self, room: Room):
        self.room = room

    def leave_room(self):
        if self.room:
            self.room.remove_player(self)
            self.room = None
