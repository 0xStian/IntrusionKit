import threading
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer

server = None  # Global reference

def start_file_server(directory, port):
    class CustomHTTPRequestHandler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=directory, **kwargs)
    
    def server_thread():
        global server
        with TCPServer(("", port), CustomHTTPRequestHandler) as httpd:
            server = httpd 
            httpd.serve_forever()

    threading.Thread(target=server_thread, daemon=True).start()

def stop_file_server():
    global server
    if server:
        server.shutdown()  # Stop loop
        server.server_close()  # Close socket
        print("Server has been stopped.")



