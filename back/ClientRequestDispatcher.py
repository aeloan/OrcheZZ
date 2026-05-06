from typing import Callable
from back.Room import Room


class ClientRequestDispatcher:
    handlers: dict[str, Callable] = {}

    @staticmethod
    def handle_create_room(client, args):
        client.client_name = args[0]
        room = Room(client)
        client.room = room
        client.send(f"ACK_CR {room.code}")

        print(f"Création salle avec args: {args}")

    @staticmethod
    def handle_join_room(client, args):
        room = next((r for r in client.manager.rooms if r.code == args[0]), None)
        client.client_name = args[1]

        if room is None:
            client.send("ERR_RR ROOM_NOT_FOUND")
            return

        if client.room is not None:
            if client.room.admin == client:
                client.send("ERR_RR ALREADY_IN_ROOM")
                return
            client.room.remove_player(client)

        client.room = room
        room.add_player(client)
        client.send(f"ACK_RR {room.code}")
        room.send_room(f"RR {args[1]}")

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

        client.send(f"ACK_PR {room.code} {' '.join([player.client_name for player in players])}")

    @staticmethod
    def handle_set_difficulty(client, args):
        room = client.room
        if room is None:
            client.send("ERR_AD ROOM_NOT_FOUND")
            return

        if room.admin != client:
            client.send("ERR_AD USER_NOT_ADMIN")
            return

        room.set_difficulty(client, args[1])
        client.send("ACK_AD")
        room.send_room(f"LD {room.difficulty}")

    @staticmethod
    def handle_get_difficulty(client, args):
        room = client.room
        if room is None:
            client.send("ERR_LD ROOM_NOT_FOUND")
            return

        client.send(f"ACK_LD {room.difficulty}")

    @staticmethod
    def handle_set_level(client, args):
        room = client.room
        if room is None:
            client.send("ERR_AL ROOM_NOT_FOUND")
            return

        if room.admin != client:
            client.send("ERR_AL USER_NOT_ADMIN")
            return

        room.set_level(client, args[1])
        client.send("ACK_AL")
        room.send_room(f"LL {room.level}")

    @staticmethod
    def handle_get_level(client, args):
        room = client.room
        if room is None:
            client.send("ERR_LL ROOM_NOT_FOUND")
            return

        client.send(f"ACK_LL {room.level}")

    @staticmethod
    def handle_start_game(client, args):
        room = client.room
        if room is None:
            client.send("ERR_SG ROOM_NOT_FOUND")
            return

        if room.admin != client:
            client.send("ERR_SG USER_NOT_ADMIN")
            return

        room.start_game()
        room.send_room("ACK_SG")

    @staticmethod
    def handle_audio(client, args):
        print(f"Audio reçu")

        room = client.room
        if room is None:
            client.send("ERR_AU ROOM_NOT_FOUND")
            return

        room.handle_client_audio(client, args)


ClientRequestDispatcher.handlers = {
    "AU": ClientRequestDispatcher.handle_audio,
    "CR": ClientRequestDispatcher.handle_create_room,
    "RR": ClientRequestDispatcher.handle_join_room,
    "PR": ClientRequestDispatcher.handle_get_room_players,
    "AD": ClientRequestDispatcher.handle_set_difficulty,
    "AL": ClientRequestDispatcher.handle_set_level,
    "LD": ClientRequestDispatcher.handle_get_difficulty,
    "LL": ClientRequestDispatcher.handle_get_level,
    "SG": ClientRequestDispatcher.handle_start_game,
}
