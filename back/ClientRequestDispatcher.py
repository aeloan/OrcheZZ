from typing import Callable


class ClientRequestDispatcher:
    handlers: dict[str, Callable] = {}

    @staticmethod
    def handle_create_room(client, args):
        print(f"Création salle avec args: {args}")

    @staticmethod
    def handle_join_room(client, args):
        print(f"Rejoindre salle avec args: {args}")


ClientRequestDispatcher.handlers = {
    "CR": ClientRequestDispatcher.handle_create_room,
    "RR": ClientRequestDispatcher.handle_join_room
}
