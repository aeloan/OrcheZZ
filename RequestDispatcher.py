class RequestDispatcher:
    def __init__(self):
        self.handlers = {
            "CR": self.handle_create_room
        }


    def handle_create_room(self):
        pass