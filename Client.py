import socket


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def connect(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            client_socket.connect((self.host, self.port))
            print(f"Connexion établie avec {self.host} sur le port {self.port}")

            client_socket.send(b"bloup")

        except ConnectionRefusedError:
            print("Erreur : Le serveur a refusé la connexion.")
        except Exception as e:
            print(f"Une erreur est survenue : {e}")

        finally:
            client_socket.close()
            print("Socket fermée.")