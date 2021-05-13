# COE 817 PROJECT: Secure Purchase Order
# Authors: Kalp Patel (500823851), Taha Gharib (500524609), Zeshan Fayyaz (500768016), Sasung Kim (500642700), Shahbaz Yousaf (500777080)

import CryptoUtil
import NetworkUtil
import ClientNetworkUtil
from Crypto.PublicKey import RSA

# Decrypts the purchase message and verifies the purchase message using both customer and supervisor public keys.
# Returns the plaintext purchase message.


def handle_supervisor_purchase_message(supervisor_connection, keypair, customer_public_key, supervisor_public_key):
    customer_signature = NetworkUtil.receive_message(supervisor_connection)
    encrypted_purchase_message = NetworkUtil.receive_message(
        supervisor_connection)
    supervisor_signature = NetworkUtil.receive_message(supervisor_connection)

    purchase_message = CryptoUtil.decrypt(
        encrypted_purchase_message, keypair).decode()
    print(f"Purchase message is: {purchase_message}")

    CryptoUtil.verify(purchase_message.encode(),
                      customer_public_key, customer_signature)
    CryptoUtil.verify(purchase_message.encode(),
                      supervisor_public_key, supervisor_signature)
    return encrypted_purchase_message, supervisor_signature, purchase_message


if __name__ == "__main__":
    # Connect to supervisor
    supervisor_connection = ClientNetworkUtil.connect_to_supervisor()
    # Generate our key pair and and get the public keys of others
    keypair, supervisor_public_key = ClientNetworkUtil.exchange_public_keys(
        supervisor_connection)
    customer_public_key = RSA.importKey(
        NetworkUtil.receive_message(supervisor_connection))

    while True:
        (encrypted_purchase_message, supervisor_signature, purchase_message) = handle_supervisor_purchase_message(supervisor_connection, keypair, customer_public_key,
                                                                                                                  supervisor_public_key)
        timestamp = purchase_message.split("|")[0]
        item = purchase_message.split("|")[1]
        print(f"Customer would like to purchase {item} at {timestamp}.")

        # Show all the received messages (encrypted)
        presentation = input(
            "Show the all sending and receiving messages? (y/n)")
        if (presentation == 'y'):
            print(f"\nSuperviosr's public key: {customer_public_key}")
            print(
                f"\nEncrypted Purchase Message: {encrypted_purchase_message}")
            print(f"\nSupervisor Signature: {supervisor_signature}")
