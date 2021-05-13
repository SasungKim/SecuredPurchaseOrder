# COE 817 PROJECT: Secure Purchase Order
# Authors: Kalp Patel (500823851), Taha Gharib (500524609), Zeshan Fayyaz (500768016), Sasung Kim (500642700), Shahbaz Yousaf (500777080)

import socket

server_ip = 'localhost'
server_port = 8000

# Server-side function to create a listening socket on the given port. Returns the listening socket.


def create_listening_socket(port):
    # Create socket for IPV4 address family and use TCP
    listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Immediately free the port after program exit
    listening_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Bind socket to self (if port is 0, then bind uses a random free port)
    listening_socket.bind(('localhost', port))
    # Set socket to listen
    listening_socket.listen()
    return listening_socket


# Server-side function to listen for inbound connections to the given listening socket. accept() blocks until a
# connection is received. Returns the inbound connection along with the client address.
def accept_connection(listening_socket):
    return listening_socket.accept()


# Client-side function to create a connection to the given ip and port. Returns the outbound connection.
def create_connection(ip, port):
    if ip == "":
        ip = server_ip
    # Create socket for IPV4 address family and use TCP
    outbound_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Immediately free the port after program exit
    outbound_connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Connect to given ip and port
    outbound_connection.connect((ip, port))
    return outbound_connection


# Send a message (bytes object) on the connection.
def send_message(connection, message):
    # Protocol is the message's byte length (padded to 5 bytes) followed by the message contents
    byte_length = len(message).to_bytes(length=5, byteorder='big')
    connection.sendall(byte_length + message)


# Receive a message (bytes object) on the connection. Blocks until data is received. Returns the data if received.
# Returns -1 if connection is closed.
def receive_message(connection):
    # Receive 5 bytes to get message byte length
    data_received = connection.recv(5, socket.MSG_WAITALL)
    if not data_received:
        return -1
    byte_length = int.from_bytes(bytes=data_received, byteorder='big')
    # Receive byte_length bytes to get message
    data_received = connection.recv(byte_length, socket.MSG_WAITALL)
    if not data_received:
        return -1

    return data_received
