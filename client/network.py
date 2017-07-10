import socket
import json
import sys

class Network():
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

    def refresh(self):
        with self.sock:
            self.sock.sendall(bytes('refresh\n', 'utf-8'))
            received = str(self.sock.recv(2**20), 'utf-8')
            received = json.loads(received)
            # received = json.loads(str(self.sock.recv(2**20), 'utf-8').strip())
            return received
            # album_database.clear()
            # album_database.update(received)

    def login(self, data):
        with self.sock:
            self.sock.sendall(bytes('login\n', 'utf-8'))
            self.sock.sendall(bytes(json.dumps(data)+"\n", "utf-8"))
            received = str(self.sock.recv(1024), "utf-8").strip()
            if received=='ok':
                return True
            else:
                print(received)
                return False

    def register(self, data):
        with self.sock:
            self.sock.sendall(bytes('register\n', 'utf-8'))
            self.sock.sendall(bytes(json.dumps(data)+"\n", "utf-8"))
            received = str(self.sock.recv(1024), "utf-8").strip()
            if received=='ok':
                return True
            else:
                print(received)
                return False

    def pay(self, data):
        with self.sock:
            print(f'purchasing with data: {data}')
            self.sock.sendall(bytes('purchase\n', 'utf-8'))
            self.sock.sendall(bytes(json.dumps(data)+"\n", "utf-8"))
            received = json.loads(str(self.sock.recv(1024*2*2*2), "utf-8").strip())
            print(f'received {received}')
            if not received['cart']:
                return True
            else:
                data['cart'].clear()
                data['cart'].update({key:value for key,value in received['cart'].items() if int(value)>0})
                return False
