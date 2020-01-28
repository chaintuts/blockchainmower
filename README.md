## General
____________

### Author
* Josh McIntyre

### Website
* jmcintyre.net

### Overview
* BlockchainMower is a Proof-of-Concept for tokenized real-world assets

## Development
________________

### Git Workflow
* master for releases (merge development)
* development for bugfixes and new features

### Building (Python and Prebuilt Firmware)
* make build
Build the application
* make clean
Clean the build directory

### Features
* Query the Bitcoin Cash blockchain for a current token owner using SLPDB
* Request a signature with a message based on asset id, owner, and timestamp
* Sign a message using a private key on a USB drive
* Verify the signature to verify ownership of the asset
* Drive a relay to start up a lawn tractor
(Could be used to drive a solenoid to open a lock, etc. Lots of possibilities for adapting this code!)

### Requirements
* Requires Python3 and Adafruit Crickit libraries

### Platforms
* Raspberry Pi

## Usage
____________

### General usage
* This prototype has several parts required for usage - Rpi with Adafruit Crickit hat, USB key, LED & switch, relay, wires set up for tractor circuit
* When properly set up, the Pi will automatically verify ownership using the USB key and signature challenge-response
* If the owner is approved, an LED will light up indicating the mower can be started
* By pushing the push button switch, the tractor will turn over!
