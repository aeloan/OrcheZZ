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

#
# @socketio.on('disconnect')
# def handle_disconnect():
#     print("Client déconnecté")
#
#     client = clients.pop(request.sid, None)
#     if client:
#         client.close()


# 👉 Exemple : créer une room
@socketio.on('RR')
def create_room():
    client = clients.get(request.sid)
    if client:
        client.send("RR")


# 👉 Exemple : rejoindre une room
@socketio.on('join_room')
def join_room(data):
    client = clients.get(request.sid)
    if client:
        room_id = data["room_id"]
        pseudo = data["pseudo"]
        client.send(f"RR {room_id} {pseudo}")


# ========================
# ROUTES (UNIQUEMENT HTML)
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

if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)