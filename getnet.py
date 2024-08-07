import requests
import json

# Configuration
infoblox_url = "https://your-infoblox-server/wapi/v2.13.4"
username = "your-username"
password = "your-password"
network = "10.197.185.0/24"

# Disable SSL warnings
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

def get_network_info(infoblox_url, network, auth):
    endpoint = f"{infoblox_url}/network?network={network}"
    try:
        response = requests.get(endpoint, auth=auth, verify=False)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response text: {response.text}")
    except Exception as err:
        print(f"An error occurred: {err}")

def get_fixed_addresses(infoblox_url, network, auth):
    endpoint = f"{infoblox_url}/fixedaddress?network={network}"
    try:
        response = requests.get(endpoint, auth=auth, verify=False)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response text: {response.text}")
    except Exception as err:
        print(f"An error occurred: {err}")

def get_leases(infoblox_url, network, auth):
    endpoint = f"{infoblox_url}/lease?network={network}"
    try:
        response = requests.get(endpoint, auth=auth, verify=False)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response text: {response.text}")
    except Exception as err:
        print(f"An error occurred: {err}")

def get_ranges(infoblox_url, network, auth):
    endpoint = f"{infoblox_url}/range?network={network}"
    try:
        response = requests.get(endpoint, auth=auth, verify=False)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response text: {response.text}")
    except Exception as err:
        print(f"An error occurred: {err}")

def main():
    auth = (username, password)
    
    # Get network information
    network_info = get_network_info(infoblox_url, network, auth)
    
    # Get fixed addresses within the network
    fixed_addresses = get_fixed_addresses(infoblox_url, network, auth)
    
    # Get leases within the network
    leases = get_leases(infoblox_url, network, auth)
    
    # Get ranges within the network
    ranges = get_ranges(infoblox_url, network, auth)
    
    if network_info and fixed_addresses and leases and ranges:
        # Create a template in JSON format
        template = {
            "network_info": network_info,
            "fixed_addresses": fixed_addresses,
            "leases": leases,
            "ranges": ranges
        }
        
        # Output the template as a JSON file
        with open('network_template.json', 'w') as json_file:
            json.dump(template, json_file, indent=4)
        
        print("Network template saved to network_template.json")
    else:
        print("Failed to retrieve some network information.")

if __name__ == "__main__":
    main()
