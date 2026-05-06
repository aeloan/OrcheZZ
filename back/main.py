import librosa
import sys
import os
from pathlib import Path

root_path = Path(__file__).parent.parent
sys.path.insert(0, str(root_path))

from back.SocketManager import SocketManager


def main():
    sock = SocketManager('localhost', 8888)
    sock.start()

if '__main__' == __name__:
    main()
