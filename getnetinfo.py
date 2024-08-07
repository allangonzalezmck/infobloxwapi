import requests
import json

# Configuration
infoblox_url = "https://your-infoblox-server/wapi/v2.10"
username = "your-username"
password = "your-password"
network = "10.197.185.0/24"

# Disable SSL warnings
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

def get_network_info(infoblox_url, network, auth):
    endpoint = f"{infoblox_url}/network?network={network}"
    response = requests.get(endpoint, auth=auth, verify=False)
    response.raise_for_status()
    return response.json()

def get_fixed_addresses(infoblox_url, network, auth):
    endpoint = f"{infoblox_url}/fixedaddress?network={network}"
    response = requests.get(endpoint, auth=auth, verify=False)
    response.raise_for_status()
    return response.json()

def get_reservations(infoblox_url, network, auth):
    endpoint = f"{infoblox_url}/reservation?network={network}"
    response = requests.get(endpoint, auth=auth, verify=False)
    response.raise_for_status()
    return response.json()

def main():
    auth = (username, password)
    
    # Get network information
    network_info = get_network_info(infoblox_url, network, auth)
    
    # Get fixed addresses within the network
    fixed_addresses = get_fixed_addresses(infoblox_url, network, auth)
    
    # Get reservations within the network
    reservations = get_reservations(infoblox_url, network, auth)
    
    # Create a template in JSON format
    template = {
        "network_info": network_info,
        "fixed_addresses": fixed_addresses,
        "reservations": reservations
    }
    
    # Output the template as a JSON file
    with open('network_template.json', 'w') as json_file:
        json.dump(template, json_file, indent=4)
    
    print("Network template saved to network_template.json")

if __name__ == "__main__":
    main()
