import socket
import os
import json

def list_files(directory, file_type):
    try:
        if file_type:  # Check if file_type is not an empty string
            files = [f for f in os.listdir(directory) if f.endswith(file_type)]
        else:
            files = os.listdir(directory)  # List all files if no file_type is provided
        return json.dumps(files)
    except Exception as e:
        return json.dumps({'error': str(e)})
    
def send_file(conn, file_path):
    try:
        with open(file_path, 'rb') as f:
            file_size = os.path.getsize(file_path)
            conn.sendall(f"{file_size}".encode() + b'\n')  # Send file size first
            conn.sendfile(f)
    except Exception as e:
        print(f"Failed to send file: {e}")

def handle_client(conn):
    while True:
        command = conn.recv(4096).decode()
        if not command:
            break
        command = json.loads(command)
        
        if action := command.get('action'):
            if action == 'list':
                response = list_files(command.get('directory'), command.get('file_type'))
                conn.sendall(response.encode())
            elif action == 'download':
                send_file(conn, command.get('file_path'))
                break
            
def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('localhost', 8001))
        s.listen()
        print("Server listening...")
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                handle_client(conn)
main()
