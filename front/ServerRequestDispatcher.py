### TEST
from typing import Callable


class ServerRequestDispatcher:
    handlers: dict[str, Callable] = {}

    @staticmethod
    def handle_create_room(client, args):
        print(f"Création salle avec args: {args}")
        client.socketio.emit("create_room", args, to=client.sid)

    @staticmethod
    def handle_join_room(client, args):
        print(f"Rejoindre salle avec args: {args}")
        client.socketio.emit("join_room", args, to=client.sid)

    @staticmethod
    def handle_leave_room(client, args):
        print(f"Quitter la salle avec args: {args}")
        client.socketio.emit("quit_room", args, to=client.sid)

    @staticmethod
    def handle_get_players_in_room(client, args):
        print(f"Récupération des joueurs dans la salle avec args: {args}")
        client.socketio.emit("get_players", args, to=client.sid)

    @staticmethod
    def handle_new_player_joined(client, args):
        print(f"Ajout d'un nouveau joueur dans la salle avec args: {args}")
        client.socketio.emit("new_player_joined", args, to=client.sid)

    @staticmethod
    def handle_get_difficulty(client, args):
        print(f"Récupération de la difficulté de la salle avec args: {args}")
        client.socketio.emit("get_diff", args, to=client.sid)

    @staticmethod
    def handle_get_niveau(client, args):
        print(f"Récupération du niveau de la salle avec args: {args}")
        client.socketio.emit("get_niveau", args, to=client.sid)

    @staticmethod
    def handle_set_difficulty(client, args):
        print(f"Changement de la difficulté de la salle avec args: {args}")
        client.socketio.emit("set_diff", args, to=client.sid)

    @staticmethod
    def handle_set_niveau(client, args):
        print(f"Changement du niveau de la salle avec args: {args}")
        client.socketio.emit("set_niveau", args, to=client.sid)

    @staticmethod
    def handle_start_game(client, args):
        print(f"Lancement de la partie: {args}")
        client.socketio.emit("start_game", args, to=client.sid)

ServerRequestDispatcher.handlers = {
    "ACK_CR": ServerRequestDispatcher.handle_create_room,
    "ACK_RR": ServerRequestDispatcher.handle_join_room,
    "RR": ServerRequestDispatcher.handle_new_player_joined,
    "ACK_LR": ServerRequestDispatcher.handle_leave_room,
    "ACK_PR": ServerRequestDispatcher.handle_get_players_in_room,
    "LD": ServerRequestDispatcher.handle_get_difficulty,
    "LL": ServerRequestDispatcher.handle_get_niveau,
    "ACK_LD": ServerRequestDispatcher.handle_get_difficulty,
    "ACK_LL": ServerRequestDispatcher.handle_get_niveau,
    "ACK_AD": ServerRequestDispatcher.handle_set_difficulty,
    "ACK_AL": ServerRequestDispatcher.handle_set_niveau,
    "ACK_SG": ServerRequestDispatcher.handle_start_game,
}

### TEST
