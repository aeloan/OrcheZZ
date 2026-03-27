import socket
from typing import Optional

from RequestDispatcher import RequestDispatcher
from Room import Room
from common.SockerFramer import SocketFramer


class ClientHandler:
    def __init__(self, socket: socket.socket, address: str, manager):
        self.socket = socket
        self.address = address
        self.manager = manager
        self.running = True
        self.room: Optional[Room] = None
        self.client_name = None

    def handle(self):
        framer = SocketFramer(self.socket)

        while self.running:
            try:
                raw_msg = framer.read_message()
                message = raw_msg.decode()
                self.process_message(message)
            except Exception as e:
                print(f"Erreur client {self.address}: {e}")
                break

        self.close()

    def process_message(self, message: str):
        parts = message.split()
        cmd = parts[0]
        args = parts[1:]

        self.dispatch(cmd=cmd, args=args)

    def dispatch(self, cmd, args):
        handler = RequestDispatcher.handlers.get(cmd)

        if handler:
            handler(self, args)
        else:
            self.send({"type": "error", "msg": "Unknown command"})


    def send(self, message: str):
        framer = SocketFramer(self.socket)

        try:
            self.socket.send(framer.write_message(message.encode()))
        except Exception as e:
            print(f"Erreur send {self.address} : {e}")
            self.close()

    def close(self):
        if self.running:
            self.running = False
            self.socket.close()
            self.manager.remove_client(self)
            self.manager = None

    def set_room(self, room: Room):
        self.room = room

    def leave_room(self):
        self.room = None
