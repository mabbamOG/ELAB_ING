import socketserver

class Server(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        self.clientip = self.client_address[0]
        print(f'connected to {clientip}')
        self.fin, self.fout = self.rfile, self.wfile
        cmd = fin.readline().strip()
        if cmd in ['']:
            pass

        # self.wfile.write(self.data.upper())

    def on_refresh(self):
        pass

    def on_login(self):
        pass

    def on_register(self):
		# cliente stesso id
		# codice fiscale
        pass

    def on_purchase(self):
        pass

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
