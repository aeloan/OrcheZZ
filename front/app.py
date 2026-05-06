import time
import sys
from flask import Flask, render_template, request
from flask_socketio import SocketIO

from pathlib import Path

# Ajouter la racine du projet au chemin Python
root_path = Path(__file__).parent.parent
sys.path.insert(0, str(root_path))

from front.ServerHandler import ServerHandler

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

clients = {}

# ========================
# WEBSOCKET
# ========================

@socketio.on('connect')
def handle_connect():
    token = request.args.get("token")


    if token in clients.keys():
        # reconnect : on réutilise le handler existant
        client = clients[token]
        client.sid = request.sid
        client.socketio = socketio
    else:
        # première connexion : créer le handler TCP
        client = ServerHandler("localhost", 8888, request.sid, socketio)
        client.connect()
        clients[token] = client


@socketio.on('disconnect')
def handle_disconnect():
    token = request.args.get("token")
    # socketio.start_background_task(delayed_cleanup, token, request.sid)


@socketio.on("audio_chunk")
def handle_audio_chunk(data):
    client = clients.get(request.args.get("token"))
    if client:
        audio_bytes = bytes(data)
        client.send(b"AU " + audio_bytes)


@socketio.on('CR')
def create_room(data):
    client = clients.get(request.args.get("token"))
    if client:
        pseudo = data.get("pseudo", "Player") if data else "Player"
        client.send(f"CR {pseudo}")


@socketio.on('RR')
def join_room(data):
    client = clients.get(request.args.get("token"))
    if client:
        room_id = data["room_id"]
        pseudo = data["pseudo"]
        client.send(f"RR {room_id} {pseudo}")


@socketio.on('LR')
def leave_room(data):
    client = clients.get(request.args.get("token"))
    if client:
        room_id = data["room_id"]
        client.send(f"LR {room_id}")


@socketio.on('PR')
def get_players_in_room(data):
    # on force à attendre un peu avant de lancer l'appel pour que le navigateur ait le temps de charger le lobby
    time.sleep(2)
    client = clients.get(request.args.get("token"))
    if client:
        room_id = data["room_id"]
        client.send(f"PR {room_id}")


@socketio.on('LD')
def get_difficulty(data):
    # on force à attendre un peu avant de lancer l'appel pour que le navigateur ait le temps de charger le lobby
    #time.sleep(2)
    client = clients.get(request.args.get("token"))
    if client:
        room_id = data["room_id"]
        client.send(f"LD {room_id}")


@socketio.on('LL')
def get_niveau(data):
    # on force à attendre un peu avant de lancer l'appel pour que le navigateur ait le temps de charger le lobby
    #time.sleep(2)
    client = clients.get(request.args.get("token"))
    if client:
        room_id = data["room_id"]
        client.send(f"LL {room_id}")


@socketio.on('AD')
def set_difficulty(data):
    client = clients.get(request.args.get("token"))
    if client:
        room_id = data["room_id"]
        difficulty = data["difficulty"]
        client.send(f"AD {room_id} {difficulty}")


@socketio.on('AL')
def set_niveau(data):
    client = clients.get(request.args.get("token"))
    if client:
        room_id = data["room_id"]
        level = data["level"]
        client.send(f"AL {room_id} {level}")


@socketio.on('SG')
def start_game(data):
    client = clients.get(request.args.get("token"))
    if client:
        client.send(f"SG")


# ========================
# ROUTES
# ========================


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/creer-partie')
def creerPartie():
    pseudo = request.args.get("pseudo")
    liste_joueurs = [
        {"pseudo": pseudo, "est_pret": True, "est_host": True},
    ]

    liste_diff = [
        {"id": "1", "label": "Difficile", "code": "difficile"},
        {"id": "2", "label": "Normal", "code": "normal"},
        {"id": "3", "label": "Facile", "code": "facile"},
    ]

    liste_niv = [
        {"id": "1", "label": "Avec partition et son", "code": "part_son"},
        {"id": "2", "label": "Avec partition", "code": "part"},
        {"id": "3", "label": "Avec son", "code": "son"},
    ]

    return render_template('lobby.html', joueurs=liste_joueurs, difficultes=liste_diff, niveaux=liste_niv, isCreation=True)


@app.route('/connexionRoom')
def connexionRoom():
    return render_template('join_room.html', pseudo=request.args.get("pseudo"))


@app.route('/join-partie')
def joinPartie():
    pseudo = request.args.get("pseudo")
    liste_joueurs = [
        {"pseudo": pseudo, "est_pret": True, "est_host": False},
    ]

    liste_diff = [
        {"id": "1", "label": "Difficile", "code": "difficile"},
        {"id": "2", "label": "Normal", "code": "normal"},
        {"id": "3", "label": "Facile", "code": "facile"},
    ]

    liste_niv = [
        {"id": "1", "label": "Avec partition et son", "code": "part_son"},
        {"id": "2", "label": "Avec partition", "code": "part"},
        {"id": "3", "label": "Avec son", "code": "son"},
    ]

    return render_template('lobby.html', joueurs=liste_joueurs, difficultes=liste_diff, niveaux=liste_niv, isCreation=False)


@app.route('/game-room')
def startPartie():
    return render_template('game_room.html')


# ========================
# RUN
# ========================


def cleanup_client(token):
    client = clients.pop(token, None)
    if client is not None:
        client.close()
        socketio.emit("invalidate_token", to=client.sid)
        del client


def delayed_cleanup(token, requestSid):
    socketio.sleep(5)

    client = clients.get(token)

    # si le client ne s'est pas reconnecté
    if client and client.sid != requestSid:
        cleanup_client(token)


def inactivity_watcher():
    TIMEOUT = 600  # secondes

    while True:
        now = time.time()

        for token, client in list(clients.items()):
            if now - client.last_activity > TIMEOUT:
                print(f"Client {token} timeout")

                try:
                    socketio.emit("timeout")
                    cleanup_client(token)
                except:
                    pass

        socketio.sleep(10)


if __name__ == '__main__':
    socketio.start_background_task(inactivity_watcher)
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)