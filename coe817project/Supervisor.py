# COE 817 PROJECT: Secure Purchase Order
# Authors: Kalp Patel (500823851), Taha Gharib (500524609), Zeshan Fayyaz (500768016), Sasung Kim (500642700), Shahbaz Yousaf (500777080)

import CryptoUtil
import NetworkUtil
from Crypto.PublicKey import RSA


def listen_for_department_and_customer():
    # Connection as Supervisor being Index Server (department and customer as clients)
    print("Supervisor will start on localhost")
    listening_socket = NetworkUtil.create_listening_socket(
        NetworkUtil.server_port)
    print("Supervisor done binding to host and port successfully")
    print("Supervisor is waiting for incoming connections")

    print("\nListening for Department...")
    department_connection, addr_dept = NetworkUtil.accept_connection(
        listening_socket)
    print(addr_dept, " Department has connected to the Supervisor and is now online...")

    print("\nListening for Customer...")
    customer_connection, addr_cust = NetworkUtil.accept_connection(
        listening_socket)
    print(addr_cust, "Customer Has connected to the Supervisor and is now online...")

    return department_connection, customer_connection


def exchange_public_keys(department_connection, customer_connection):
    keypair = CryptoUtil.generate_keypair()

    # Send Supervisor Public key to Department and Customer
    NetworkUtil.send_message(department_connection,
                             keypair.public_key().exportKey())  # Department
    NetworkUtil.send_message(
        customer_connection, keypair.public_key().exportKey())  # Customer

    # Gather Public Keys from Department and Customer
    department_public_key = RSA.importKey(
        NetworkUtil.receive_message(department_connection))
    customer_public_key = RSA.importKey(
        NetworkUtil.receive_message(customer_connection))

    # Send Customer Public key to Department
    NetworkUtil.send_message(department_connection,
                             customer_public_key.exportKey())

    return keypair, department_public_key, customer_public_key


# Received the encrypted message with signature. Decrypt the message ande verify the signature.
def handle_customer_purchase_message_and_confirm(customer_connection, keypair, customer_public_key):
    encrypted_purchase_message = NetworkUtil.receive_message(
        customer_connection)
    customer_signature = NetworkUtil.receive_message(customer_connection)

    purchase_message = CryptoUtil.decrypt(
        encrypted_purchase_message, keypair).decode()
    print(f"Purchase message is: {purchase_message}")

    CryptoUtil.verify(purchase_message.encode(),
                      customer_public_key, customer_signature)

    timestamp = purchase_message.split("|")[0]
    item = purchase_message.split("|")[1]
    print(f"Customer would like to purchase {item} at {timestamp}.")

    confirmation = input(f"Confirm the above purchase? (y/n) ")
    return confirmation, customer_signature, purchase_message, encrypted_purchase_message


def reencrypt_and_resign_purchase_message_to_department(department_connection, customer_signature, purchase_message,
                                                        department_public_key):
    # Resend customer signature to deparmtent
    NetworkUtil.send_message(department_connection, customer_signature)

    # Re-encrypt purchase message using the department's public key, generate our own signature and send both to
    # the department
    encrypted_purchase_message = CryptoUtil.encrypt(
        purchase_message.encode(), department_public_key)
    supervisor_signature = CryptoUtil.sign(purchase_message.encode(), keypair)
    NetworkUtil.send_message(department_connection, encrypted_purchase_message)
    NetworkUtil.send_message(department_connection, supervisor_signature)


if __name__ == "__main__":
    # Connect to department and customer
    department_connection, customer_connection = listen_for_department_and_customer()
    # Generate our key pair and and get the public keys of others
    keypair, department_public_key, customer_public_key = exchange_public_keys(department_connection,
                                                                               customer_connection)

    while True:
        confirmation, customer_signature, purchase_message, encrypted_purchase_message = handle_customer_purchase_message_and_confirm(
            customer_connection, keypair, customer_public_key)

        if confirmation == 'y':
            # Tell customer that order is confirmed
            confirmation_msg = CryptoUtil.encrypt(
                "Order was confirmed".encode(), customer_public_key)
            NetworkUtil.send_message(customer_connection, confirmation_msg)

            reencrypt_and_resign_purchase_message_to_department(department_connection, customer_signature,
                                                                purchase_message, department_public_key)
        else:
            # Rejected order
            confirmation_msg = CryptoUtil.encrypt(
                "Order was rejected".encode(), customer_public_key)
            NetworkUtil.send_message(customer_connection, confirmation_msg)

        # Show all the received messages (encrypted)
        presentation = input(
            "Show the all sending and receiving messages? (y/n)")
        if (presentation == 'y'):
            print(f"\nCustomer's public key: {customer_public_key}")
            print(f"\nDepartment's public key: {department_public_key}")
            print(f"\nPurchase message: {encrypted_purchase_message}")
            print(f"\nCustomer's signature: {customer_signature}")
            print(f"\nConfirmation Message: {confirmation_msg}")
