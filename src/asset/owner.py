# This file contains code that fetches and caches tokenized asset owner information
#
# Author: Josh McIntyre
#

import requests
import json

# Module constants
CACHE_FILE = "owner.txt"
ID_FILE = "assetid.txt"
QUERY_FILE = "query.txt"
NETWORK_CHECK_URL = "https://duckduckgo.com"

# This function loads the cached owner address from file
def load_owner_cache():

    with open(CACHE_FILE) as f:
        owner = f.readline().replace("\n", "")
        return owner

# Load the current owning address from an SLPDB instance
def load_owner_network():

    with open(QUERY_FILE) as f:
        query = f.readline().replace("\n", "")
    
    ret = requests.get(query)
    
    data = json.loads(ret.text)
    data = data.get("a") # SLPDB JSON key for the address list
    for address_data in data:
        address = address_data.get("address")
        
        # The Blockchain Mower token only has 1 token issued
        # So the address with a token balance of 1 is the current owner
        balance = address_data.get("token_balance")
        if balance == "1":
            return address

# This function loads the cached asset id from file
def load_assetid_cache():

    with open(ID_FILE) as f:
        assetid = f.readline().replace("\n", "")
        return assetid
        
# Basic helper to check if we can reach the internet
def is_network_on():

    try:
        ret = requests.get(NETWORK_CHECK_URL, timeout=1)
        return True
    except requests.exceptions.Timeout:
        return False

# Wrapper that will fetch the owner from the chain or a cache file
def load_owner():

    if is_network_on():
        return load_owner_network()
    else:
        return load_owner_cache()

# Wrapper that will fetch the asset id from the chain or a cache file
def load_assetid():

    return load_assetid_cache()
    

