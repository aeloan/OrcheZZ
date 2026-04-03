from typing import Callable
import io

from back.Room import Room


class ClientRequestDispatcher:
    handlers: dict[str, Callable] = {}

    @staticmethod
    def handle_create_room(client, args):
        room = Room(client)
        client.send("ACK_CR " + room.code)

        print(f"Création salle avec args: {args}")

    @staticmethod
    def handle_join_room(client, args):
        room = client.manager.rooms.find(args)
        if room is None:
            client.send("ERR_RR ROOM_NOT_FOUND")
            return

        if client.room is not None:
            if client.room.admin == client:
                client.send("ERR_RR ALREADY_IN_ROOM")
                return
            client.room.remove_player(client)

        room.add_player(client)
        client.send("ACK_RR")

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
