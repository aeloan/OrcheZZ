import json


class Protocol:

    @staticmethod
    def encode(data: dict) -> bytes:
        return (json.dumps(data) + "\n").encode()

    @staticmethod
    def decode(data: bytes) -> dict:
        return json.loads(data.decode())
