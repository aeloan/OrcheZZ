import asyncio
import random
import string
import threading

from back.MusicScoreScorer import compare_notes, mix_audios

notes = ["A", "B", "C", "D", "E", "F", "G"]

NB_ROUNDS = 5


class Room:
    def __init__(self, admin):
        self.admin = admin
        self.players = [admin]
        self.admin.manager.rooms.append(self)
        choices = string.ascii_uppercase + string.digits
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
            # Crée une tâche asynchrone qui tourne en arrière-plan dans un thread séparé
            threading.Thread(target=lambda: asyncio.run(self.game_loop()), daemon=True).start()

    async def game_loop(self):
        for i in range(NB_ROUNDS):
            await asyncio.sleep(2)
            self.init_round()
            # On attend 5 secondes sans bloquer les autres joueurs/salons
            await asyncio.sleep(5)
            self.end_round()
        self.running = False
        self.send_room(f"EG")

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
            self.score_game[key] += (val / NB_ROUNDS) * 100

        final_audio = mix_audios(self.round_audios.values())
        if final_audio and len(final_audio) > 0:
            audio_bytes = final_audio.export(format="webm").read()
            self.send_room(b"AR " + audio_bytes)
        else:
            self.send_room("AR")

    def handle_client_audio(self, client_caller, audio_bytes: bytes):
        if self.running:
            self.round_audios[client_caller] = audio_bytes
            score = compare_notes(audio_bytes, self.current_note)
            self.score_round[client_caller] = score
