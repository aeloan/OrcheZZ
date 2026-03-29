import socket
from typing import Callable

from common.BaseHandler import BaseHandler
from common.SockerFramer import SocketFramer
from front.ServerRequestDispatcher import ServerRequestDispatcher


class ServerHandler(BaseHandler):
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        super().__init__(self.socket)

    def connect(self):
        self.socket.connect((self.host, self.port))
        print("Connecté au serveur")
        self.framer = SocketFramer(self.socket)
        self.start()

    def get_dispatcher(self) -> dict[str, Callable]:
        return ServerRequestDispatcher.handlers
