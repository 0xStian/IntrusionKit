import socket
import os
import json

def send_command(command, ipaddress, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((f'{ipaddress}', int(port)))
        s.sendall(command.encode())
        response = s.recv(4096).decode()
    return response


def request_file(directory, file_name, ipaddress, port):
    file_path = os.path.join(directory, file_name)  #TODO: Adjust to send full path
    command = json.dumps({'action': 'download', 'file_path': file_path})
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((f'{ipaddress}', int(port)))
        s.sendall(command.encode())
        file_size_info = s.recv(4096).decode().strip()
        if file_size_info:
            file_size = int(file_size_info)
            received = 0
            with open(file_name, 'wb') as f:
                while received < file_size:
                    data = s.recv(4096)
                    if not data:
                        break
                    received += len(data)
                    f.write(data)
            print(f"Downloaded {file_name}")
        else:
            print("Failed to get file size. Ensure the server is correctly sending the file size.")


def retrieve_documents(directory, file_type, ipaddress, port):
    if file_type == "":
        command = json.dumps({'action': 'list', 'directory': directory})
    else:
        command = json.dumps({'action': 'list', 'directory': directory, 'file_type': file_type})
    response = send_command(command, ipaddress, port)
    files = json.loads(response)
    return files


#TODO: possibly add feature to view files content before transfer