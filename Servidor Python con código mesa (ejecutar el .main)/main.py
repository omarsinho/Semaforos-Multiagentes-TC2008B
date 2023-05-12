"""
    Script to create a server which calls the model.step from
    an MAS implementation

    From unity side, you can watch this video:
    https://www.youtube.com/watch?v=GIxu8kA9EBU

"""


# Install pyngrok to propagate the http server
# pip install pyngrok 

# Load the required packages
from pyngrok        import ngrok
from http.server    import BaseHTTPRequestHandler, HTTPServer

import json
import logging
import os

# Import MAS module
from sistema_final import Ciudad

# Invoke model
x_size = 510 # en metros
y_size = 510 # en metros
cars = 700 # número de autos

model = Ciudad(x_size, y_size, cars)

class Server(BaseHTTPRequestHandler):
    
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", 
                     str(self.path), str(self.headers))
        self._set_response()
        response = model.step()
        self.wfile.write(response.encode('utf-8'))

    def do_POST(self):
        pass

def run(server_class=HTTPServer, handler_class=Server, port=8585):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)

    public_url = ngrok.connect(port).public_url
    logging.info(f"ngrok tunnel \"{public_url}\" -> \"http://127.0.0.1:{port}\"")

    logging.info("Starting httpd...\n") # HTTPD is HTTP Daemon!
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:   # CTRL + C stops the server
        pass

    httpd.server_close()
    logging.info("Stopping httpd...\n")


if __name__ == "__main__":
    # server
    run(HTTPServer, Server)
    
    
    
    
