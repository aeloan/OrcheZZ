import socket
from typing import Optional

from Protocol import Protocol
from Room import Room


class ClientHandler:
    def __init__(self, socket: socket.socket, address: str, manager):
        self.socket = socket
        self.address = address
        self.manager = manager
        self.running = True
        self.room: Optional[Room] = None

    def handle(self):
        while self.running:
            try:
                data = self.socket.recv(1024)
                if not data:
                    break

                message = Protocol.decode(data=data)

                # TODO (envoyer les infos à la room, créer/rejoindre une salle, ...)

            except Exception as e:
                print(f"Erreur client {self.address} : {e}")
                break

        self.close()

    def send(self, data: dict):
        try:
            self.socket.send(Protocol.encode(data))
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
