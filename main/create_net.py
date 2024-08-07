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

def create_network(infoblox_url, auth, network_data):
    """
    Create a new network in Infoblox.
    
    :param infoblox_url: Base URL for Infoblox WAPI.
    :param auth: Tuple of (username, password) for authentication.
    :param network_data: Dictionary containing network configuration data.
    :return: Response from the Infoblox WAPI.
    """
    endpoint = f"{infoblox_url}/network"
    payload = {
        "comment": network_data['comment'],
        "network": network_data['address'],
        "options": [
            {
                "name": "dhcp-lease-time",
                "num": 51,
                "use_option": network_data['options']['dhcp-lease-time']['use_option'],
                "value": "43200",
                "vendor_class": "DHCP"
            }
        ]
    }
    try:
        response = requests.post(endpoint, auth=auth, json=payload, verify=False)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response text: {response.text}")
    except Exception as err:
        print(f"An error occurred: {err}")

def create_network_container(infoblox_url, auth, network_container_data):
    """
    Create a new network container in Infoblox.
    
    :param infoblox_url: Base URL for Infoblox WAPI.
    :param auth: Tuple of (username, password) for authentication.
    :param network_container_data: Dictionary containing network container configuration data.
    :return: Response from the Infoblox WAPI.
    """
    endpoint = f"{infoblox_url}/networkcontainer"
    payload = {
        "network": network_container_data['network'],
        "start_addr": network_container_data['start_addr'],
        "end_addr": network_container_data['end_addr']
    }
    try:
        response = requests.post(endpoint, auth=auth, json=payload, verify=False)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response text: {response.text}")
    except Exception as err:
        print(f"An error occurred: {err}")

def main():
    """
    Main function to load configuration, check for existing network, and create network and network container.
    """
    auth = (username, password)
    
    # Load configuration from YAML file
    config = load_yaml_config('/scripts/infoblox/variables.yml')
    
    # Define the network address
    network = config['network']['address']
    
    # Pre-check if the network exists
    network_ref = check_network_exists(infoblox_url, auth, network)
    if network_ref:
        print(f"Network already exists in Infoblox: {network_ref}")
        return
    
    # Create network
    network_data = {
        "comment": config['network']['comment'],
        "address": config['network']['address'],
        "options": config['network']['options']
    }
    network_response = create_network(infoblox_url, auth, network_data)
    print(f"Network creation response: {network_response}")
    
    # Create network container
    network_container_response = create_network_container(infoblox_url, auth, config['network_container'])
    print(f"Network container creation response: {network_container_response}")

if __name__ == "__main__":
    main()
