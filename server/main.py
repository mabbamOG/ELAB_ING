import socketserver
import osZZk

class Server(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def __init__(self):
        socketserver.BaseRequestHandler.__init__()

    def load_db(self):
        with open('



    def handle(self):
        self.clientip = self.client_address[0]
        print(f'connected to {clientip}')
        self.fin, self.fout = self.rfile, self.wfile
        cmd = fin.readline().strip()
        if cmd == 'refresh':
            self.on_refresh
        elif cmd == 'login':
            self.on_login
        elif cmd == 'register':
            self.on_register
        elif cmd == 'buy':
            self.on_purchase
        else:
            raise 'error: server could not handle!'

    def on_refresh(self):


    def on_login(self):
        pass

    def on_register(self):
        pass
    
    def on_purchase(self):
        pass

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    with open('/home/mad/Documents/000/ELAB-ING/client/database.json') as f:
        database = json.loads(f.read())

    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
