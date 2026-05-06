import librosa
from back.SocketManager import SocketManager


def main():
    sock = SocketManager('localhost', 8888)
    sock.start()

if '__main__' == __name__:
    main()
