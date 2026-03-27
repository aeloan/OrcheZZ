class RequestDispatcher:
    handlers = {}

    @staticmethod
    def handle_create_room(client, args):
        print(f"Création salle avec args: {args}")

    @staticmethod
    def handle_join_room(client, args):
        print(f"Rejoindre salle avec args: {args}")


RequestDispatcher.handlers = {
    "CR": RequestDispatcher.handle_create_room,
    "RR": RequestDispatcher.handle_join_room
}
