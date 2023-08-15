# This is a simple script to start a quick tcp client

import socket

target_host = "127.0.0.1" # This is the target machine
target_port = 9998 # This is the target port

# Create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the client
client.connect((target_host, target_port))

# Send some data
client.send(b"TEST TEST TEST TEST") # The b is for byte string. You can change this to fit your needs. Accepted formats are string, byte string, and byte array.

# Receive some data
response = client.recv(4096) # This is the maximum amount of data to receive at once. You can change this to fit your needs.

# Print the response
print(response.decode())
client.close()