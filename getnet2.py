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

def get_dhcp_status(infoblox_url, network, auth):
    endpoint = f"{infoblox_url}/network?network={network}&_return_fields=dhcp_members"
    try:
        response = requests.get(endpoint, auth=auth, verify=False)
        response.raise_for_status()
        network_info = response.json()
        dhcp_disabled = not network_info[0].get('dhcp_members', [])
        return dhcp_disabled
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response text: {response.text}")
    except Exception as err:
        print(f"An error occurred: {err}")

def get_reverse_mapping_zone_status(infoblox_url, network, auth):
    endpoint = f"{infoblox_url}/network?network={network}&_return_fields=enable_create_reversezone"
    try:
        response = requests.get(endpoint, auth=auth, verify=False)
        response.raise_for_status()
        network_info = response.json()
        reverse_mapping_zone = network_info[0].get('enable_create_reversezone', False)
        return reverse_mapping_zone
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response text: {response.text}")
    except Exception as err:
        print(f"An error occurred: {err}")

def main():
    auth = (username, password)
    
    # Get network information
    network_info = get_network_info(infoblox_url, network, auth)
    
    # Get DHCP status
    dhcp_disabled = get_dhcp_status(infoblox_url, network, auth)
    
    # Get reverse mapping zone status
    reverse_mapping_zone = get_reverse_mapping_zone_status(infoblox_url, network, auth)
    
    if network_info is not None and dhcp_disabled is not None and reverse_mapping_zone is not None:
        # Create a template in JSON format
        template = {
            "network_info": network_info,
            "dhcp_disabled": dhcp_disabled,
            "enable_create_reversezone": reverse_mapping_zone
        }
        
        # Output the template as a JSON file
        with open('network_template.json', 'w') as json_file:
            json.dump(template, json_file, indent=4)
        
        print("Network template saved to network_template.json")
    else:
        print("Failed to retrieve some network information.")

if __name__ == "__main__":
    main()
