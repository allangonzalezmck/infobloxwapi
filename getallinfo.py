import requests
import json

# Configuration
infoblox_url = "https://your-infoblox-server/wapi/v2.13.4"
username = "your-username"
password = "your-password"
network = "10.197.185.0/24"

# Disable SSL warnings
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

def get_detailed_network_info(infoblox_url, network, auth):
    endpoint = f"{infoblox_url}/network?network={network}&_return_fields=network_view,comment,enable_create_reversezone,options,extattrs"
    try:
        response = requests.get(endpoint, auth=auth, verify=False)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response text: {response.text}")
    except Exception as err:
        print(f"An error occurred: {err}")

def get_network_container_info(infoblox_url, network, auth):
    endpoint = f"{infoblox_url}/networkcontainer?network={network}"
    try:
        response = requests.get(endpoint, auth=auth, verify=False)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response text: {response.text}")
    except Exception as err:
        print(f"An error occurred: {err}")

def get_address_range_info(infoblox_url, network, auth):
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
    
    # Get detailed network information
    network_info = get_detailed_network_info(infoblox_url, network, auth)
    
    # Get network container information
    network_container_info = get_network_container_info(infoblox_url, network, auth)
    
    # Get address range information
    address_range_info = get_address_range_info(infoblox_url, network, auth)
    
    if network_info or network_container_info or address_range_info:
        # Create a template in JSON format
        template = {
            "network_info": network_info,
            "network_container_info": network_container_info,
            "address_range_info": address_range_info
        }
        
        # Output the template as a JSON file
        with open('network_comprehensive_info.json', 'w') as json_file:
            json.dump(template, json_file, indent=4)
        
        print("Comprehensive network information saved to network_comprehensive_info.json")
    else:
        print("Failed to retrieve some network information.")

if __name__ == "__main__":
    main()
