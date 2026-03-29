import socket
from abc import ABC, abstractmethod
import threading
from typing import Callable

from common.SockerFramer import SocketFramer


class BaseHandler(ABC):
    def __init__(self, socket: socket.socket):
        self.socket = socket
        self.running = True
        self.framer = SocketFramer(self.socket)

    def start(self):
        threading.Thread(target=self.listen, daemon=True).start()

    def listen(self):
        while self.running:
            try:
                raw_msg = self.framer.read_message()
                message = raw_msg.decode()
                self.process_message(message)
            except Exception as e:
                print(f"Erreur : {e}")
                break

        self.close()

    def process_message(self, message: str):
        parts = message.split()
        cmd = parts[0]
        args = parts[1:]

        self.dispatch(cmd=cmd, args=args)

    def dispatch(self, cmd, args):
        handler = self.get_dispatcher().get(cmd)

        if handler:
            handler(self, args)
        else:
            self.send(str({"type": "error", "msg": "Unknown command"}))

    def send(self, message: str):
        try:
            framed_message = SocketFramer.write_message(message.encode())
            self.socket.send(framed_message)
        except Exception as e:
            print(f"Erreur send : {e}")
            self.close()

    def close(self):
        if self.running:
            self.running = False
            self.socket.close()

    @abstractmethod
    def get_dispatcher(self) -> dict[str, Callable]:
        pass
