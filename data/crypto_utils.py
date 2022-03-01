#!/usr/bin/env python3

from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA512, SHA
from base64 import b64decode
import argparse

'''
# Usage example:

# pip install pycryptodome

key_pair = generate_key_pair()
message = "Hello, World."
signature_hex_string = sign(message, key_pair)
# signature_hex_string can be sent to server

pub_key_export = export_public_key(key_pair)
# pub_key_export can be sent to server or saved for later use.

fingerprint = export_public_key_fingerprint(key_pair)
# fingerprint can be sent to the server.

# this signature check is performed by the server:
check_signature(pub_key_export, signature_hex_string, message)

priv_key_export = export_private_key(key_pair)
# priv_key_export can be saved for later use, then it can be imported with:
key_pair_only_private_half = import_private_key(priv_key_export)
# this key_pair_only_private_half can then be used for other signatures as above.

# formerly exported public key can be imported with:
key_pair_only_public_half = import_public_key(pub_key_export)

'''


def generate_key_pair():
    key_pair = RSA.generate(bits = 4096)
    return key_pair

# the the bytes of a string in utf-8 encoding
def utf(message: str) -> bytes:
    return bytes(message, 'utf-8')

#returns a signature of the given message, with the signatures bytes encoded as hex string
def sign(message: str, key_pair) -> str:
    #generate the hash that will be signed:
    msg_hash = SHA512.new(utf(message))
    signer = PKCS1_v1_5.new(key_pair)
    signature_bytes = signer.sign(msg_hash)
    signature_hex_string = signature_bytes.hex()
    return signature_hex_string

# exports the public key encoded as base64 string without padding and newlines as defined in the API.
def export_public_key(key_pair):
    b64_bytes = key_pair.publickey().exportKey()
    b64_string = b64_bytes.decode()
    # remove padding:
    b64_string = b64_string.replace("-----BEGIN PUBLIC KEY-----", "")
    b64_string = b64_string.replace("-----END PUBLIC KEY-----", "")
    # remove newlines:
    b64_string = b64_string.replace("\n", "")
    return b64_string

# imports a public key that has been exported with the function above.
# returns: a keypair, with the private half being empty
def import_public_key(b64_pubkey: str):
    pub_key = RSA.importKey(b64decode(b64_pubkey))
    return pub_key

def export_public_key_fingerprint(key_pair):
    b64_string = export_public_key(key_pair)
    fingerprint = SHA.new(utf(b64_string))
    return fingerprint.hexdigest()

def export_private_key(key_pair):
    b64_bytes = key_pair.exportKey()
    b64_string = b64_bytes.decode()
    #remove padding:
    b64_string = b64_string.replace("-----BEGIN RSA PRIVATE KEY-----", "")
    b64_string = b64_string.replace("-----END RSA PRIVATE KEY-----", "")
    #remove newlines:
    b64_string = b64_string.replace("\n", "")
    return b64_string

# imports a private key that has been exported with the function above.
# returns: a keypair, with the public half being empty. can be used to sign data.
def import_private_key(b64_pubkey: str):
    priv_key = RSA.importKey(b64decode(b64_pubkey))
    return priv_key

def check_signature(pub_key_b64, signature_bytes_hexstring, message_string):
    """
    Verifies the given signature of the SHA512 hash of the given message_string with the given key.

    Parameters:
    pub_key_b64 (```str```): the public key as base64 encoded string without padding.
    signature_bytes_hexstring (```str```): the bytes for the signature encoded as hex-string.
        This is received in this format from front end.
    message_string (```str```): the data that has been signed. More specifically: its SHA512 hash has been signed.

    Raises Exception: if the signature is invalid or the key or the signature cannot be read.

    """

    pub_key = RSA.importKey(b64decode(pub_key_b64))
    verifier = PKCS1_v1_5.new(pub_key)
    sig_bytes = bytes(bytearray().fromhex(signature_bytes_hexstring))
    # signature is not made for the raw message but its hash:
    message_hash = SHA512.new(bytes(message_string, 'utf-8'))

    if(verifier.verify(message_hash, sig_bytes)):
        print("Valid signature.")
    else:
        raise Exception("Invalid signature '%s' for data '%s'" % (signature_bytes_hexstring, message_string))
