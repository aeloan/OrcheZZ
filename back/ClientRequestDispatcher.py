from typing import Callable
import io

class ClientRequestDispatcher:
    handlers: dict[str, Callable] = {}

    @staticmethod
    def handle_create_room(client, args):
        print(f"Création salle avec args: {args}")

    @staticmethod
    def handle_join_room(client, args):
        print(f"Rejoindre salle avec args: {args}")

    @staticmethod
    def handle_audio(client, args):
        print(f"Audio reçu")
        # TODO
        # with open("enregistrement.webm", "wb") as f:
        #     f.write(args)


ClientRequestDispatcher.handlers = {
    "AU": ClientRequestDispatcher.handle_audio,
    "CR": ClientRequestDispatcher.handle_create_room,
    "RR": ClientRequestDispatcher.handle_join_room
}
