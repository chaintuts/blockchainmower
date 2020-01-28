# This file contains code for sending and verifying challenge-response signature requests
# for a blockchain-tradeable lawnmower
#
# Author: Josh McIntyre
#
import time
import hashlib
import base64
import os
import subprocess

from electron_cash_lib.bitcoin import verify_message

import owner

# This function generates a signing request message
def generate_message_request(asset_id, owning_address, timestamp):

    # Generate a signing request message based on the asset id, current owner, and current Unix timestamp
    # This will ensure the signature will need to be relatively recent in order to be considered valid
    raw_string = f"{asset_id}{owning_address}{timestamp}"
    raw_string = raw_string.encode("utf-8")
    req_string = hashlib.sha256(raw_string)
    req_string = req_string.hexdigest()

    return req_string

# Helper function to get the USB media path on the Raspberry pi
# This simply looks for the name of a mounted device in /media/pi and isn't particularly robust
def get_usb_path():

    MEDIA_PATH = "/media/pi"
    SIGNING_SCRIPT = "sign.py"

    mounted = os.listdir(MEDIA_PATH)
    for device in mounted:
        if SIGNING_SCRIPT in os.listdir(os.path.join(MEDIA_PATH, device)):
            path = os.path.join(MEDIA_PATH, device, SIGNING_SCRIPT)
            return path

# This function will send a signing request to a USB thumb drive containing the signing python code
# This particular version is more for proof of concept, because a USB drive communicates directly with
# the device running this code and doesn't keep private keys gapped like a hardware wallet or smartcard would
def send_signing_request_usb(owning_address, message):

        PYTHON_BIN = "python3"

        # Get the signing script path
        usb_path = get_usb_path()
        if not usb_path:
            raise Exception("Unable to connect to signing device")

        # Execute the signing script
        ret = subprocess.run([PYTHON_BIN, usb_path, message, owning_address], capture_output=True)

        signature = ret.stdout
        return signature

# Send the signing request and receive the signature or an Exception
def send_signing_request(owning_address, message):

    try:
        signature = send_signing_request_usb(owning_address, message)
    except Exception as e:
        raise Exception(f"Error with signing request {e}") from e

    return signature

# The driver function that generates a signing request, sends it, and verifies the result
def generate_and_verify():

    asset_id = owner.load_assetid()
    owning_address = owner.load_owner()
    timestamp = time.time()

    req_string = generate_message_request(asset_id, owning_address, timestamp)
    print(f"Generated signing request for\nAsset ID: {asset_id}\nOwned by: {owning_address}\nTimestamp: {timestamp}\nSigning request message: {req_string}")

    signature = send_signing_request(owning_address, req_string)
    print(f"Signature returned by device: {signature}")
    
    verified = verify_message(owning_address, base64.b64decode(signature), req_string.encode("utf-8"))
    if verified:
        print(f"Signature successfully verified! Asset is owned by {owning_address}")
    else:
        print("Signature is invalid. Cannot prove asset ownership")
        
    return verified
