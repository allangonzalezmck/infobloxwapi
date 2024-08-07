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
    endpoint = f"{infoblox_url}/network?network={network}&_return_fields=disable_dhcp,enable_create_reversezone"
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
    
    if network_info:
        network_data = network_info[0]
        dhcp_disabled = network_data.get('disable_dhcp', False)
        reverse_mapping_zone = network_data.get('enable_create_reversezone', False)
        
        # Create a template in JSON format
        template = {
            "network_info": network_data,
            "dhcp_disabled": dhcp_disabled,
            "enable_create_reversezone": reverse_mapping_zone
        }
        
        # Output the template as a JSON file
        with open('network_template.json', 'w') as json_file:
            json.dump(template, json_file, indent=4)
        
        print("Network template saved to network_template.json")
    else:
        print("Failed to retrieve network information.")

if __name__ == "__main__":
    main()
