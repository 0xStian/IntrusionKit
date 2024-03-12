import socket
import os
import json

def send_command(command):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('localhost', 12345))
        s.sendall(command.encode())
        response = s.recv(1024).decode()
    return response

def list_files(directory, file_type):
    command = json.dumps({'action': 'list', 'directory': directory, 'file_type': file_type})
    response = send_command(command)
    files = json.loads(response)
    return files


def request_file(directory, file_name, files):
    if file_name in files:
        file_path = os.path.join(directory, file_name)  #TODO: Adjust to send full path
        command = json.dumps({'action': 'download', 'file_path': file_path})
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('localhost', 8002))
            s.sendall(command.encode())
            file_size_info = s.recv(1024).decode().strip()
            if file_size_info:
                file_size = int(file_size_info)
                received = 0
                with open(file_name, 'wb') as f:
                    while received < file_size:
                        data = s.recv(1024)
                        if not data:
                            break
                        received += len(data)
                        f.write(data)
                print(f"Downloaded {file_name}")
            else:
                print("Failed to get file size. Ensure the server is correctly sending the file size.")
    else:
        print("File not found in the listed files. Please enter a file name from the list.")

def retrieve_documents(directory, file_type):
    print (directory, file_type)
    files = list_files(directory, file_type)

    if files:
        print("Files found:", files)
        file_name = input("Enter file name to download (from listed files): ")
        if file_name in files:
            request_file(directory, file_name, files)
        else:
            print("File not found in the listed files. Please enter a file name from the list.")
    else:
        print("No files found or an error occurred.")


#TODO: possibly add feature to view files content before transfer