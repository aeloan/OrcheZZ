class Protocol:
    @staticmethod
    def encode(data: str) -> bytes:
        return (data + "\n").encode()

    @staticmethod
    def decode(data: str) -> str:
        return data