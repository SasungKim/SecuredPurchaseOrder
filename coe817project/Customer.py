# COE 817 PROJECT: Secure Purchase Order
# Authors: Kalp Patel (500823851), Taha Gharib (500524609), Zeshan Fayyaz (500768016), Sasung Kim (500642700), Shahbaz Yousaf (500777080)

import CryptoUtil
import NetworkUtil
import ClientNetworkUtil
from datetime import datetime

# Returns a string in the form of "time_stamp|item" where time_stamp is datetime and item is what the customer wants to
# purchase. Example of a return value is "2021-04-04 23:47:40|HP EliteBook 840 G7 Laptop".


def ask_user_for_purchase_message():
    items = ["HP EliteBook 840 G7 Laptop", "Lenovo ThinkPad T480 Laptop", "Dell OptiPlex 3050 Micro Desktop PC",
             "Dell P2419H 24 Inch Monitor", "Microsoft Ergonomic Keyboard"]

    print("Welcome to the Secure Purchase Order system.")
    print("Listed below are the items currently available in stock.")
    for i in range(len(items)):
        print(f"{i}. {items[i]}")
    item_index = int(
        input("Please enter the associated number to purchase an item: "))

    return datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "|" + items[item_index]


# Encrypt and sign a purchase message. Then send to supervisor. Returns the confirmation (y/n).
def send_purchase_to_supervisor(supervisor_connection, purchase_message, keypair, supervisor_public_key):
    # Encrypt purchase message with supervisor's public key
    encrypted_purchase_message = CryptoUtil.encrypt(
        purchase_message.encode(), supervisor_public_key)
    # Sign purchase message with our private key
    signature = CryptoUtil.sign(purchase_message.encode(), keypair)

    NetworkUtil.send_message(supervisor_connection, encrypted_purchase_message)
    NetworkUtil.send_message(supervisor_connection, signature)

    confirmation = NetworkUtil.receive_message(supervisor_connection)
    return encrypted_purchase_message, signature, confirmation


if __name__ == "__main__":
    # Connect to supervisor
    supervisor_connection = ClientNetworkUtil.connect_to_supervisor()
    # Generate our key pair and get the supervisor's public key
    keypair, supervisor_public_key = ClientNetworkUtil.exchange_public_keys(
        supervisor_connection)

    while True:
        # Ask the user for an item to purchase and get the purchase message
        purchase_message = ask_user_for_purchase_message()
        print(f"Purchase message is: {purchase_message}")

        # Send purchase to supervisor
        (encrypted_purchase_message, signature, confirmation) = send_purchase_to_supervisor(
            supervisor_connection, purchase_message, keypair, supervisor_public_key)

        confirmation_msg = CryptoUtil.decrypt(confirmation, keypair).decode()
        print(confirmation_msg)

        # Show all the received messages (encrypted)
        presentation = input(
            "Show the all receiving messages? (y/n)")
        if (presentation == 'y'):
            print(f"\nSupervisor's public key: {supervisor_public_key}", )
            print(f"\nEncrypted order Message: {encrypted_purchase_message}")
            print(
                f"\nConfirmation message from supervisor: {confirmation}")
