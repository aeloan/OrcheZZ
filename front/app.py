import time

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

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
    cleanup_client(token)


@socketio.on("audio_chunk")
def handle_audio_chunk(data):
    client = clients.get(request.args.get("token"))
    if client:
        audio_bytes = bytes(data)
        client.send(b"AU " + audio_bytes)


# 👉 Exemple : créer une room
@socketio.on('RR')
def create_room():
    client = clients.get(request.args.get("token"))
    if client:
        client.send("RR")


# 👉 Exemple : rejoindre une room
@socketio.on('join_room')
def join_room(data):
    client = clients.get(request.args.get("token"))
    if client:
        room_id = data["room_id"]
        pseudo = data["pseudo"]
        client.send(f"RR {room_id} {pseudo}")


# ========================
# ROUTES
# ========================

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/creer-partie')
def creerPartie():
    return render_template('lobby.html')


@app.route('/connexionRoom')
def connexionRoom():
    return render_template('temp.html')


# ========================
# RUN
# ========================

def cleanup_client(token):
    client = clients.pop(token)
    if client:
        client.close()
        socketio.emit("invalidate_token")
        del client


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