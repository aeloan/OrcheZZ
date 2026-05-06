import random
import string
import threading
from asyncio import sleep

from back.MusicScoreScorer import compare_notes, mix_audios

notes = ["A", "B", "C", "D", "E", "F", "G"]


class Room:
    def __init__(self, admin):
        self.admin = admin
        self.players = [admin]
        self.admin.manager.rooms.add(self)
        choices = string.ascii_letters + string.digits
        self.code = ''.join(random.choice(choices) for i in range(5))
        self.running = False
        self.difficulty = 0
        self.level = 0
        self.score_round = {}
        self.score_game = {}
        self.round_audios = {}
        self.current_note = None

    def add_player(self, client):
        if not self.running:
            self.players.append(client)
            client.set_room(self)

    def remove_player(self, client):
        if not self.running and client in self.players:
            self.players.remove(client)

    def start_game(self):
        if not self.running:
            self.running = True
            self.score_game = {p: 0 for p in self.players}
            threading.Thread(target=self.game_loop, daemon=True).start()

    def game_loop(self):
        while self.running:
            self.init_round()
            sleep(5)
            self.end_round()

    def send_room(self, message: str | bytes):
        for p in self.players:
            p.send(message)

    def set_difficulty(self, client_caller, difficulty_code):
        if not self.running and self.admin == client_caller:
            self.difficulty = difficulty_code

    def set_level(self, client_caller, level_code):
        if not self.running and self.admin == client_caller:
            self.level = level_code

    def init_round(self):
        self.current_note = random.choice(notes)
        self.score_round = {p: 0 for p in self.players}
        self.round_audios = {p: None for p in self.players}
        self.send_room(f"RS {self.current_note}")

    def end_round(self):
        for key, val in self.score_round.items():
            self.score_game[key] += val

        final_audio = mix_audios(self.round_audios.values())
        self.send_room(f"AR {final_audio}")

    def handle_client_audio(self, client_caller, audio_bytes: bytes):
        if self.running:
            self.round_audios[client_caller] = audio_bytes
            score = compare_notes(audio_bytes, self.current_note)
            self.score_round[client_caller] = score
