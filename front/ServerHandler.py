import socket
import time
from typing import Callable

from common.BaseHandler import BaseHandler
from common.SockerFramer import SocketFramer
from front.ServerRequestDispatcher import ServerRequestDispatcher


class ServerHandler(BaseHandler):
    def __init__(self, host: str, port: int, sid, socketio):
        self.host = host
        self.port = port
        self.sid = sid
        self.socketio = socketio
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.last_activity = time.time()
        super().__init__(self.socket)

    def connect(self):
        self.socket.connect((self.host, self.port))
        print("Connecté au serveur")
        self.framer = SocketFramer(self.socket)
        self.start()

    def get_dispatcher(self) -> dict[str, Callable]:
        return ServerRequestDispatcher.handlers

    def send(self, message: str | bytes):
        self.last_activity = time.time()
        super().send(message)