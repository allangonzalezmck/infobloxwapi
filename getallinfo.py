import requests
import json

# Configuration
infoblox_url = "https://your-infoblox-server/wapi/v2.13.4"
username = "your-username"
password = "your-password"
network = "10.197.185.0/24"

# Disable SSL warnings
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

def get_all_network_info(infoblox_url, network, auth):
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

def main():
    auth = (username, password)
    
    # Get all network information
    network_info = get_all_network_info(infoblox_url, network, auth)
    
    if network_info:
        # Output all network information as a JSON file
        with open('network_all_info.json', 'w') as json_file:
            json.dump(network_info, json_file, indent=4)
        
        print("All network information saved to network_all_info.json")
    else:
        print("Failed to retrieve network information.")

if __name__ == "__main__":
    main()
