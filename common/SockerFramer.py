import socket

class SocketFramer:
    def __init__(self, sock: socket.socket):
        self.sock = sock
        self.buffer = b""
        self.bufferSize = 1024

    def read_message(self) -> bytes:
        while b"\n" not in self.buffer:
            data = self.sock.recv(self.bufferSize)
            if not data:
                raise ConnectionResetError
            self.buffer += data

        header, self.buffer = self.buffer.split(b"\n", 1)
        size = int(header.decode())

        while len(self.buffer) < size:
            data = self.sock.recv(self.bufferSize)
            if not data:
                raise ConnectionResetError

            self.buffer += data

        message = self.buffer[:size]
        self.buffer = self.buffer[size:]
        return message

    @staticmethod
    def write_message(message: bytes) -> bytes:
        header = f"{len(message)}\n".encode()
        return header + message
