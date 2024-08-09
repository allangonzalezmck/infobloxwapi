import requests

# Configuration
infoblox_url = "https://your-infoblox-server/wapi/v2.13.4"
username = "your-username"
password = "your-password"

# Disable SSL warnings
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

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
    except Exception as err:
        print(f"An error occurred: {err}")
        return None

def main():
    auth = (username, password)
    
    # List of subnets to process
    network_list = ["10.0.0.0"]  # Update required subnet here

    # Iterate over each network (subnet) in the list
    for network in network_list:
        print(f"Processing network: {network}")
        
        # Iterate over IP addresses 1 to 10 within the current subnet
        for i in range(1, 11):
            ip_add_parts = network.split('.')[:3]
            ip_base = '.'.join(ip_add_parts)
            ip_address = f"{ip_base}.{i}"
            
            print(f"\tChecking IP address: {ip_address}")
            
            # Check if the fixed address exists
            if check_fixed_address_exists(infoblox_url, auth, ip_address):
                print(f"\tReservation exists for {ip_address}")
            else:
                # Create the fixed address (reservation) if it doesn't exist
                create_response = create_fixed_address(infoblox_url, auth, ip_address)
                if create_response:
                    print(f"\tCreated reservation for {ip_address}")
                else:
                    print(f"\tFailed to create reservation for {ip_address}")

if __name__ == "__main__":
    main()
