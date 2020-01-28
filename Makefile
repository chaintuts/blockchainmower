# This file contains a make script for the BlockchainMower application
#
# Author: Josh McIntyre
#

# This block defines makefile variables
VERIFY_FILES=src/core/*.py
LIB_DIR=src/electron_cash_lib
USB_DIR=src/usb
ASSET_DIR=src/asset
DRIVE_FILES=src/drive/*.py

BUILD_DIR=bin/blockchainmower

# This rule builds the application
build: $(VERIFY_FILES) $(LIB_DIR) $(USB_DIR) $(ASSET_DIR) $(DRIVE_FILES)
	mkdir -p $(BUILD_DIR)
	cp $(VERIFY_FILES) $(BUILD_DIR)
	cp -r $(LIB_DIR) $(BUILD_DIR)
	cp -r $(USB_DIR)/* $(BUILD_DIR)
	cp -r $(ASSET_DIR)/* $(BUILD_DIR)
	cp $(DRIVE_FILES) $(BUILD_DIR)

# This rule cleans the build directory
clean: $(BUILD_DIR)
	rm -r $(BUILD_DIR)/*
	rmdir $(BUILD_DIR)
