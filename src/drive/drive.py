# This file contains code that drives a device based on proven blockchain ownership
#
# Author: Josh McIntyre
#

import time
from adafruit_crickit import crickit

# Device initialization and module constants
ss = crickit.seesaw

green = crickit.SIGNAL2
start = crickit.SIGNAL1
relay = crickit.SIGNAL3
ss.pin_mode(green, ss.OUTPUT)
ss.pin_mode(start, ss.INPUT_PULLUP)
ss.pin_mode(relay, ss.OUTPUT)

VALID_APPROVAL_TIME = 30 # seconds

# This is the main function for device driving
# It will loop indefinitely, checking for device ownership
# When ownership is validated, the approval is good for a set period of time
def drive():

    # Importing all the necessary libraries in verify can be slow on the PI
    # Let the user know we're initializing
    print("Initializing blockchain device verification. This may take a minute...")
    import verify

    while(True):

        # First, get proof of ownership of the asset on the blockchain
        # This will be done via a challenge-response digital signature
        print("Checking device ownership...")
        is_owner = verify.generate_and_verify()
        print(f"Finished ownership check: {is_owner}")

        # If ownership is validated, get the time of approval
        approval_time = time.time()

        # While the approval is valid, allow the start button to be pressed
        # Light up an LED indicating approval is valid during this time
        while(time.time() - approval_time < VALID_APPROVAL_TIME):
            
            # Light up the LED green
            ss.digital_write(green, True)

            # Detect button press and activate the relay or solenoid (depending on implementation)
            if not ss.digital_read(start):
                ss.digital_write(relay, True)
            else:
                ss.digital_write(relay, False)

        # The ownership check has expired
        # Stop the LED and go around again
        print("Ownership check expired")
        ss.digital_write(green, False)

# The main entry point for this blockchain device controller program
if __name__ == "__main__":

    drive()


