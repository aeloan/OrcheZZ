from typing import Callable
import io

from back.Room import Room


class ClientRequestDispatcher:
    handlers: dict[str, Callable] = {}

    @staticmethod
    def handle_create_room(client, args):
        client.client_name = args
        room = Room(client)
        client.send("ACK_CR " + room.code)

        print(f"Création salle avec args: {args}")

    @staticmethod
    def handle_join_room(client, args):
        room = client.manager.rooms.find(args)
        client.client_name = args
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
        room.send_room("RR", args)

        print(f"Rejoindre salle avec args: {args}")

    @staticmethod
    def handle_get_room_players(client, args):
        room = client.room
        if room is None:
            client.send("ERR_PR ROOM_NOT_FOUND")
            return

        players = room.players
        if players is None or len(players) == 0:
            client.send("ERR_PR NO_PLAYERS")
            return

        client.send("ACK_PR", " ".join([player.client_name for player in players]))

    @staticmethod
    def handle_set_difficulty(client, args):
        room = client.room
        if room is None:
            client.send("ERR_AD ROOM_NOT_FOUND")
            return

        if room.admin != client:
            client.send("ERR_AD USER_NOT_ADMIN")
            return

        room.set_difficulty(client, args)
        client.send("ACK_AD")
        room.send_room("LD", room.difficulty)

    @staticmethod
    def handle_get_difficulty(client, args):
        room = client.room
        if room is None:
            client.send("ERR_LD ROOM_NOT_FOUND")
            return

        client.send("ACK_LD", room.difficulty)

    @staticmethod
    def handle_set_level(client, args):
        room = client.room
        if room is None:
            client.send("ERR_AL ROOM_NOT_FOUND")
            return

        if room.admin != client:
            client.send("ERR_AL USER_NOT_ADMIN")
            return

        room.set_level(client, args)
        client.send("ACK_AL")
        room.send_room("LL", room.level)

    @staticmethod
    def handle_get_level(client, args):
        room = client.room
        if room is None:
            client.send("ERR_LL ROOM_NOT_FOUND")
            return

        client.send("ACK_LL", room.level)


    @staticmethod
    def handle_audio(client, args):
        print(f"Audio reçu")
        # TODO
        # with open("enregistrement.webm", "wb") as f:
        #     f.write(args)


ClientRequestDispatcher.handlers = {
    "AU": ClientRequestDispatcher.handle_audio,
    "CR": ClientRequestDispatcher.handle_create_room,
    "RR": ClientRequestDispatcher.handle_join_room,
    "PR": ClientRequestDispatcher.handle_get_room_players,
    "AD": ClientRequestDispatcher.handle_set_difficulty,
    "AL": ClientRequestDispatcher.handle_set_level,
    "LD": ClientRequestDispatcher.handle_get_difficulty,
    "LL": ClientRequestDispatcher.handle_get_level,
}
