import requests
import json

# Configurations (input from vRO)
infoblox_url = inputs["infoblox_url"]
username = inputs["username"]
password = inputs["password"]
network = inputs["network"]

# Authentication
auth = (username, password)

def check_network_exists(infoblox_url, auth, network):
    endpoint = f"{infoblox_url}/network?network={network}"
    response = requests.get(endpoint, auth=auth, verify=False)
    response.raise_for_status()
    network_info = response.json()
    if network_info:
        return network_info[0]['_ref']
    return None

def create_network(infoblox_url, auth, network):
    endpoint = f"{infoblox_url}/network"
    payload = {"network": network, "disable": True}
    response = requests.post(endpoint, auth=auth, json=payload, verify=False)
    response.raise_for_status()
    return response.json()

def create_fixed_address(infoblox_url, auth, ip_address):
    endpoint = f"{infoblox_url}/fixedaddress"
    payload = {"ipv4addr": ip_address, "match_client": "RESERVED"}
    response = requests.post(endpoint, auth=auth, json=payload, verify=False)
    response.raise_for_status()
    return response.json()

network_ref = check_network_exists(infoblox_url, auth, network)
if network_ref:
    print(f"Network {network} already exists: {network_ref}")
else:
    create_network(infoblox_url, auth, network)
    print(f"Network {network} created successfully.")
    for i in range(1, 11):
        ip_address = f"{network.split('.')[0]}.{network.split('.')[1]}.{network.split('.')[2]}.{i}"
        create_fixed_address(infoblox_url, auth, ip_address)
        print(f"Created reservation for {ip_address}")

# Return outputs
outputs = {"status": "success"}
