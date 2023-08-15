# Creates a quick udp client to send a message to the server
import socket

target_host = "127.0.0.1" # This is the target address that we want to send data to
target_port = 9998 # This is the target port that we want to send data to

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Send some data
sock.sendto(b"AAABBBCCC", (target_host, target_port)) # The sendto() method for UDP sockets takes two parameters: the data and the address of the target

# Receive some data
data, addr = sock.recvfrom(4096) # The recvfrom() method for UDP sockets takes one parameter: the maximum amount of data to be received at once (in bytes)

# Print the data
print(data.decode())
sock.close()