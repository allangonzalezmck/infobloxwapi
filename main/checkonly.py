import requests
import yaml

# Configuration
infoblox_url = "https://your-infoblox-server/wapi/v2.13.4"
username = "your-username"
password = "your-password"

# Disable SSL warnings
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

def load_yaml_config(file_path):
    """
    Load configuration from a YAML file.
    
    :param file_path: Path to the YAML file.
    :return: Parsed YAML data as a dictionary.
    """
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def check_network_exists(infoblox_url, auth, network):
    """
    Check if the network already exists in Infoblox.
    
    :param infoblox_url: Base URL for Infoblox WAPI.
    :param auth: Tuple of (username, password) for authentication.
    :param network: Network address to check.
    :return: Reference ID (_ref) of the network if it exists, otherwise None.
    """
    endpoint = f"{infoblox_url}/network?network={network}"
    try:
        response = requests.get(endpoint, auth=auth, verify=False)
        response.raise_for_status()
        network_info = response.json()
        if network_info:
            return network_info[0]['_ref']
        return None
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response text: {response.text}")
    except Exception as err:
        print(f"An error occurred: {err}")
    return None

def main():
    """
    Main function to load configuration and check for existing networks.
    """
    auth = (username, password)
    
    # Load configuration from YAML file
    config = load_yaml_config('/scripts/infoblox/variables.yml')
    
    # Iterate over the list of networks
    for network_data in config['networks']:
        network = network_data['address']
        
        # Pre-check if the network exists
        network_ref = check_network_exists(infoblox_url, auth, network)
        if network_ref:
            print(f"Network {network} already exists in Infoblox: {network_ref}")
        else:
            print(f"Network {network} is available for creation.")
    
if __name__ == "__main__":
    main()
