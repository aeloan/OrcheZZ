### TEST
from typing import Callable


class ServerRequestDispatcher:
    handlers: dict[str, Callable] = {}

    @staticmethod
    def handle_create_room(client, args):
        print(f"Création salle avec args: {args}")

    @staticmethod
    def handle_join_room(client, args):
        print(f"Rejoindre salle avec args: {args}")


ServerRequestDispatcher.handlers = {
    "CR": ServerRequestDispatcher.handle_create_room,
    "RR": ServerRequestDispatcher.handle_join_room
}

### TEST