import requests
import json

# Configuration
infoblox_url = "https://your-infoblox-server/wapi"
username = "your-username"
password = "your-password"

# Disable SSL warnings
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

def get_wapi_version(infoblox_url, auth):
    response = requests.get(infoblox_url, auth=auth, verify=False)
    response.raise_for_status()
    return response.json()

def main():
    auth = (username, password)
    
    # Get WAPI version
    wapi_info = get_wapi_version(infoblox_url, auth)
    
    # Print WAPI version information
    print(json.dumps(wapi_info, indent=4))

if __name__ == "__main__":
    main()






--------------------




import requests
import json

# Configuration
infoblox_url = "https://your-infoblox-server/wapi"
username = "your-username"
password = "your-password"

# Disable SSL warnings
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

def get_wapi_version(infoblox_url, auth):
    try:
        response = requests.get(infoblox_url, auth=auth, verify=False)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

def main():
    auth = (username, password)
    
    # Get WAPI version
    wapi_info = get_wapi_version(infoblox_url, auth)
    
    if wapi_info is not None:
        # Print WAPI version information
        print(json.dumps(wapi_info, indent=4))
    else:
        print("Failed to retrieve WAPI version information.")

if __name__ == "__main__":
    main()

