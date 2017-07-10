import socketserver
import os
import json
import sys

class ServerHandler(socketserver.StreamRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """


    def load_db(self):
        with open(f'{self.dbpath}/album_database.json') as f:
            self.album_database = json.loads(f.read())
        with open(f'{self.dbpath}/user_database.json') as f:
            self.user_database = json.loads(f.read())
        with open(f'{self.dbpath}/availability_database.json') as f:
            self.availability_database = json.loads(f.read())
        for key,value in self.album_database.items():
            if key not in self.availability_database:
                self.availability_database[key] = 0

    def dump_db(self):
        with open(f'{self.dbpath}/album_database.json', 'w') as f:
            f.write(json.dumps(self.album_database, indent=True, sort_keys=True))
        with open(f'{self.dbpath}/user_database.json', 'w') as f:
            f.write(json.dumps(self.user_database, indent=True, sort_keys=True))
        with open(f'{self.dbpath}/availability_database.json', 'w') as f:
            f.write(json.dumps(self.availability_database, indent=True, sort_keys=True))

    def handle(self):
        self.dbpath = os.path.dirname(os.path.realpath(__file__))
        self.load_db()
        clientip = self.client_address[0]
        print(f'connected to {clientip}')
        self.fin, self.fout = self.rfile, self.wfile
        cmd = self.fin.readline().strip().decode()
        if cmd == 'refresh':
            self.on_refresh()
        elif cmd == 'login':
            self.on_login()
        elif cmd == 'register':
            self.on_register()
        elif cmd == 'purchase':
            self.on_purchase()
        else:
            raise Exception('error: server could not handle!')

    def on_refresh(self):
        print('refreshing...')
        self.fout.write(bytes(json.dumps(self.album_database)+'\n', 'utf-8'))

    def on_login(self):
        print('logging in..')
        login_data = json.loads(self.fin.readline().strip().decode())
        if login_data['username'] in self.user_database and login_data['password'] == self.user_database[login_data['username']]['password']:
            self.fout.write(b'ok')
        else:
            self.fout.write(b'error')

    def on_register(self):
        print('registering...')
        register_data = json.loads(self.fin.readline().strip().decode())
        if register_data['username'] not in self.user_database and register_data['password']==register_data['password2']:
            self.fout.write(b'ok')
            self.user_database[register_data['username']] = register_data
            self.dump_db()
        else:
            self.fout.write(b'error')

    def on_purchase(self):
        print('purchasing..')
        purchase_data = json.loads(self.fin.readline().strip().decode())
        error = True
        if purchase_data['purchase_method'].lower() in ['credit cart','bancomat','paypal'] and purchase_data['shipping_method'].lower() in ['post','courier']:
            error = False
            for key,value in list(purchase_data['cart'].items()):
                if int(value)> int(self.availability_database[key]):
                    error = True
                    purchase_data['cart'][key] = self.availability_database[key]
        if error == False:
            print('purchase success!')
            purchase_data['cart'].clear()
            self.fout.write(bytes(json.dumps(purchase_data)+'\n', 'utf-8'))
        else:
            print(f'purchase error with result {purchase_data}')
            self.fout.write(bytes(json.dumps(purchase_data)+'\n', 'utf-8'))


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    with open('/home/mad/Documents/000/ELAB-ING/client/database.json') as f:
        database = json.loads(f.read())

    # Create the server, binding to localhost on port 9999
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer((HOST, PORT), ServerHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        try:
            server.serve_forever()
        except:
            print('aborting!')
            sys.exit()
            # server.socket.shutdown(socket.SHUT_RDWR)
            # server.socket.close()
