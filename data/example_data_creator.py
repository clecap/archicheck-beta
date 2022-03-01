#!/usr/bin/env python3

from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA512, SHA
from base64 import b64decode
import argparse
import datetime

'''
# Usage example:

$ pip install pycryptodome

for first time use ->

$ python3 example_data_creator.py
$ python3 example_data_creator.py --save_key_to_file somefile.txt

or for signing with old key ->

$ python3 example_data_creator.py --get_key_from_file keys_power-factchecker.txt
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

if __name__== "__main__":

    parser = argparse.ArgumentParser('Parse configuration file')
    parser.add_argument('--get_key_from_file', default=None, type=str)
    parser.add_argument('--save_key_to_file', default=None, type=str)
    args = parser.parse_args()
    file = args.get_key_from_file
    save = args.save_key_to_file

    pub_key_b64 = None
    priv_key = None
    key_pair = None
    publisher = None
    if file:
        with open(file, 'r') as reader:
            # Further file processing goes here
            reader.readline()
            pub_key_b64 = reader.readline()
            reader.readline()
            priv_key = reader.readline()
            reader.readline()
            fingerprint = reader.readline()
            reader.readline()
            publisher = reader.readline()
            #print("key: ", priv_key)
            key_pair = import_private_key(priv_key)
    else:
        print("generating key, pls wait ...")
        key_pair = generate_key_pair()
        save = input("textfile for possibly saving new key? (pls end with '.txt') >")
    print("key: ", key_pair)

    pub_key_b64 = export_public_key(key_pair)
    #print("\n pub key: ", pub_key_b64)
    priv_key_export = export_private_key(key_pair)
    #print("\n priv key: ", priv_key_export)
    fingerprint = export_public_key_fingerprint(key_pair)
    print("\n pub fingerprint: ",fingerprint)
    if file == None or save != None:
        if 'yes' == input("want to save key? possibly overwrites old key in file! confirm with yes (you will receive confirmation 'saved') >"):
            with open(save, 'w') as writer:
                # Further file processing goes here

                writer.write("pub key \n")
                writer.write(pub_key_b64)
                writer.write("\n")
                writer.write("priv key \n")
                writer.write(priv_key_export)
                writer.write("\n")
                writer.write("fingerprint pub key \n")
                writer.write(fingerprint)
                writer.write("\n")
                if not publisher:
                    publisher = input("factchecker name >")
                writer.write("publisher \n")
                writer.write(publisher)
                writer.write("\n")
                signatureOnPublicKeyPublisherName = sign(pub_key_b64+publisher, key_pair)
                writer.write("signatureOnPublicKeyPublisherName \n")
                writer.write(signatureOnPublicKeyPublisherName)
                writer.write("\n")

                writer.write("easy peasy copying : \n")
                writer.write("curl -d '")
                writer.write('{"createAccount":{"publicKey":"')
                writer.write(pub_key_b64)
                writer.write('","fingerPrintPublicKey":"')
                writer.write(fingerprint)
                writer.write('","publisherName":"')
                if not publisher:
                    publisher = input("factchecker name >")
                writer.write(publisher)
                ##### put in your first login manually #####
                now = datetime.datetime.now()
                iso_time = now.strftime("%Y-%m-%dT%H:%M:%SZ")
                writer.write('","firstLogin":"')
                writer.write(iso_time)
                writer.write('","signatureOnPublicKeyPublisherName":"')
                writer.write(signatureOnPublicKeyPublisherName)
                writer.write('"}}')
                writer.write("' localhost:8080/postendpoint")
                print("saved")



    in_put = input(" check or sign or stop? >")
    while in_put != 'stop':
        if in_put == 'check':
            try:
                signature = input("signed message >")
                message = input("supposed message >")
                check_signature(pub_key_b64, signature, message)
            except Exception as e:
                print(str(e))
        elif in_put == 'sign':
            message = input("message u want signed >")
            signature_hex_string = sign(message, key_pair)
            print("\n signature: ", signature_hex_string)
        in_put = input(" check or sign or stop? >")
