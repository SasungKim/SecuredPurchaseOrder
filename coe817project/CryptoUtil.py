# COE 817 PROJECT: Secure Purchase Order
# Authors: Kalp Patel (500823851), Taha Gharib (500524609), Zeshan Fayyaz (500768016), Sasung Kim (500642700), Shahbaz Yousaf (500777080)

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256


# Generate and return a 2048-bit RSA key pair (public key and private key). Returned keypair can be passed as a private
# key. Returned keypair.publickey() can be passed as a public key.
def generate_keypair():
    return RSA.generate(2048)


# Encrypt the message using PKCS#1 OAEP (RSA) with given public or private key.
def encrypt(plaintext, key):
    encryptor = PKCS1_OAEP.new(key)
    ciphertext = encryptor.encrypt(plaintext)
    return ciphertext


# Decrypt the message using PKCS#1 OAEP (RSA) with given public or private key.
def decrypt(ciphertext, key):
    decryptor = PKCS1_OAEP.new(key)
    plaintext = decryptor.decrypt(ciphertext)
    return plaintext


# Create a signature using PKCS#1 v1.5 (RSA) with a given message and private key. Note that PKCS#1 v1.5 is only used
# for signatures as using it for ciphers is not secure.
def sign(message, private_key):
    hashed_message = SHA256.new(message)
    signature = pkcs1_15.new(private_key).sign(hashed_message)
    return signature


# Verify the message with given public key and signature.
def verify(message, public_key, signature):
    hashed_mesage = SHA256.new(message)

    try:
        pkcs1_15.new(public_key).verify(hashed_mesage, signature)
        print("Signature verification succesful.")
    except (ValueError, TypeError):
        print("Signature verification failed!")
