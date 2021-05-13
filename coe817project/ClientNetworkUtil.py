# COE 817 PROJECT: Secure Purchase Order
# Authors: Kalp Patel (500823851), Taha Gharib (500524609), Zeshan Fayyaz (500768016), Sasung Kim (500642700), Shahbaz Yousaf (500777080)

import CryptoUtil
import NetworkUtil
from Crypto.PublicKey import RSA


# Returns a connection to the supervisor
def connect_to_supervisor():
    # Connecting to supervisor
    host = input("Please enter the hostname of the supervisor: ")
    connection = NetworkUtil.create_connection(host, NetworkUtil.server_port)
    print("Connected to Supervisor...")
    return connection


# Returns a generated key pair and the supervisor public key
def exchange_public_keys(connection):
    keypair = CryptoUtil.generate_keypair()

    # Send department public key to supervisor
    NetworkUtil.send_message(connection, keypair.public_key().exportKey())

    # Receive public key from supervisor
    supervisor_public_key = RSA.importKey(
        NetworkUtil.receive_message(connection))

    return keypair, supervisor_public_key
