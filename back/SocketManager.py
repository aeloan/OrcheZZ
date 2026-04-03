import socket
import threading

from ClientHandler import ClientHandler


class SocketManager:

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.rooms = []

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()

        while True:
            print("Attente d'un nouveau client...")
            client_socket, addr = self.server_socket.accept()
            client = ClientHandler(client_socket, addr, self)
            print(f"Nouveau client : {client.address}")
            self.clients.append(client)
            client.start()

    def broadcast(self, message: dict, sender):
        for client in self.clients:
            if client != sender:
                client.send(message)

    def remove_client(self, client: ClientHandler):
        if client in self.clients:
            self.clients.remove(client)
