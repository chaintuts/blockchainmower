# This code signs a message request, proving ownership of a tokenized asset
# This module is part of a proof-of-concept, and isn't the most secure way of generating
# the signature, since the keys would be accessible to the verifying device (Electron Cash
# stores a wallet on the USB filesystem, unlike a hardware wallet)
#
# Author: Josh McIntyre
#
import sys
import base64

from electron_cash_lib.bitcoin import deserialize_privkey, regenerate_key

PRIVKEY_FILE = "privkey.txt"

# Load the private key from file
def load_privkey_file():

    with open(PRIVKEY_FILE) as f:
        privkey = f.readline()
        privkey = privkey.replace("\n", "")
        return privkey

# Fulfill the signing request using the owning key
def sign_request_electron(owning_address, message):

    signature = ""

    # First, fetch and decode the WIF key
    privkey_wif = load_privkey_file()
    _, privkey, compressed = deserialize_privkey(privkey_wif)
    ec_key = regenerate_key(privkey)

    # Create an EC Key instance and sign the message
    signature = ec_key.sign_message(message, compressed)
    signature = base64.b64encode(signature)

    return signature

# The main entry point for the USB device signing code
def main():

    # Get the signing request message and address from the args
    # If they're not present, fail immediately
    try:
        message = sys.argv[1]
        owning_address = sys.argv[2]
    except IndexError:
        print("Signing request message and owning address are required.")
        sys.exit(1)

    # Get the signature and return via stdout
    signature = sign_request_electron(owning_address, message)
    print(signature.decode())

if __name__ == "__main__":
    main()
