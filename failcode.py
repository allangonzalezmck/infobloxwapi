import requests
import yaml

# Configuration
infoblox_url = "https://your-infoblox-server/wapi/v2.10"
username = "your-username"
password = "your-password"
network = "10.197.185.0/24"

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
        "network": network_data['address'],
        "comment": network_data.get('comment', ''),
        "disable": True
            }
    try:
        response = requests.post(endpoint, auth=auth, json=payload, verify=False)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response text: {response.text}")
        return None
    except Exception as err:
        print(f"An error occurred: {err}")
        return None

def create_fixed_address(infoblox_url, auth, ip_address):
    """
    Create a new fixed address (reservation) in Infoblox.

    :param infoblox_url: Base URL for Infoblox WAPI.
    :param auth: Tuple of (username, password) for authentication.
    :param ip_address: IP address to create a reservation for.
    :return: Response from the Infoblox WAPI.
    """
    endpoint = f"{infoblox_url}/fixedaddress"
    payload = {
        "ipv4addr": ip_address
        # Add more fields here if needed, such as MAC address, name, etc.
    }
    try:
        response = requests.post(endpoint, auth=auth, json=payload, verify=False)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response text: {response.text}")
        return None
    except Exception as err:
        print(f"An error occurred: {err}")
        return None

def main():
    """
    Main function to load configuration, check for existing networks, create networks, and create IP reservations.
    """
    auth = (username, password)

    # Load configuration from YAML file
    config = load_yaml_config('variables.yml')

    # Iterate over the list of networks
    for network_data in config['networks']:
        network = network_data['address']

        # Pre-check if the network exists
        network_ref = check_network_exists(infoblox_url, auth, network)
        if network_ref:
            print(f"Network {network} already exists in Infoblox: {network_ref}")
        else:
            print(f"Network {network} is available for creation.")
            # Create the network since it does not exist
            create_response = create_network(infoblox_url, auth, network_data)
            if create_response:
                print(f"Network {network} created successfully.")

                # Automatically create fixed addresses for the first 10 IPs in the network
                ip_base = '.'.join(network.split('.')[:3])
                for i in range(1, 11):
                    ip_address = f"{ip_base}.{i}"
                    create_fixed_address(infoblox_url, auth, ip_address)
                    print(f"Created reservation for {ip_address}")
            else:
                print(f"Failed to create network {network}.")

if __name__ == "__main__":
    main()
