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
    :return: Boolean indicating if the network exists and the network reference if it exists.
    """
    endpoint = f"{infoblox_url}/network?network={network}"
    try:
        response = requests.get(endpoint, auth=auth, verify=False)
        response.raise_for_status()
        network_info = response.json()
        if len(network_info) > 0:
            return True, network_info[0]['_ref']
        return False, None
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response text: {response.text}")
        return False, None
    except Exception as err:
        print(f"An error occurred: {err}")
        return False, None

def check_fixed_address_exists(infoblox_url, auth, ip_address):
    """
    Check if a fixed address (reservation) exists for a given IP address in Infoblox.
    
    :param infoblox_url: Base URL for Infoblox WAPI.
    :param auth: Tuple of (username, password) for authentication.
    :param ip_address: IP address to check.
    :return: Boolean indicating if the fixed address exists.
    """
    endpoint = f"{infoblox_url}/fixedaddress?ipv4addr={ip_address}"
    try:
        response = requests.get(endpoint, auth=auth, verify=False)
        response.raise_for_status()
        fixed_address_info = response.json()
        return len(fixed_address_info) > 0  # Returns True if fixed address exists, False otherwise
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response text: {response.text}")
        return False
    except Exception as err:
        print(f"An error occurred: {err}")
        return False

def main():
    auth = (username, password)
    
    # Load configuration from YAML file
    config = load_yaml_config('/scripts/infoblox/variables.yml')
    print("Loaded configuration:", config)  # Debug print

    # Check if 'networks' key is in the loaded config
    if 'networks' not in config:
        print("'networks' key not found in the configuration")
        return
    
    # Ensure 'networks' is a list
    if not isinstance(config['networks'], list):
        print("'networks' should be a list in the configuration")
        return

    # Iterate over the list of networks
    for network_data in config['networks']:
        # Ensure each network data is a dictionary
        if not isinstance(network_data, dict):
            print(f"Invalid network data format: {network_data}")
            continue

        print("Processing network data:", network_data)  # Debug print
        network = network_data.get('address')
        
        if not network:
            print("Network address is missing in network data:", network_data)
            continue

        # Pre-check if the network exists
        network_exists, network_ref = check_network_exists(infoblox_url, auth, network)
        if network_exists:
            print(f"Network {network} already exists in Infoblox: {network_ref}")
            
            # Automatically check the first 10 IP addresses in the network
            ip_base = '.'.join(network.split('.')[:3])
            for i in range(1, 11):
                ip_address = f"{ip_base}.{i}"
                if check_fixed_address_exists(infoblox_url, auth, ip_address):
                    print(f"\tReservation exists for {ip_address}")
                else:
                    print(f"\tReservation does not exist for {ip_address}")
        else:
            print(f"Network {network} does not exist in Infoblox.")
    
if __name__ == "__main__":
    main()
