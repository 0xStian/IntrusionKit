import socket

def send_command(command, ipaddress, port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        # Convert to bytes
        command_bytes = command.encode('utf-8')
        
        # Send command
        udp_socket.sendto(command_bytes, (ipaddress, int(port)))
        
        # Wait for a response
        data, _ = udp_socket.recvfrom(4096)
        return data.decode('utf-8')
