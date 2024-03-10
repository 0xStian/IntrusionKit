import socket

def send_command(command, ipaddress, port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        command_bytes = command.encode('utf-8')
        udp_socket.sendto(command_bytes, (ipaddress, int(port)))
        data, _ = udp_socket.recvfrom(65536) 
        return data.decode('utf-8')
