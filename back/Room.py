import random
import string
import threading


class Room:
    def __init__(self, admin):
        self.admin = admin
        self.players = [admin]
        self.admin.manager.rooms.append(self)
        choices = string.ascii_letters + string.digits
        self.code = ''.join(random.choice(choices) for i in range(5))
        self.running = False
        self.difficulty = 0
        self.level = 0

    def add_player(self, client):
        self.players.append(client)
        client.set_room(self)

    def remove_player(self, client):
        if client in self.players:
            self.players.remove(client)

    def start_game(self):
        if not self.running:
            self.running = True
            threading.Thread(target=self.game_loop, daemon=True).start()

    def game_loop(self):
        while self.running:
            # # TODO : update état du jeu
            # state = {"type": "state", "players": [id(p) for p in self.players]}
            # send_room(state)
            # import time
            # time.sleep(1)
            pass

    def send_room(self, state):
        for p in self.players:
            p.send(state)

    def set_difficulty(self, client_caller, difficulty_code):
        if self.admin == client_caller:
            self.difficulty = difficulty_code

    def set_level(self, client_caller, level_code):
        if self.admin == client_caller:
            self.level = level_code
