import requests
import json

# Path to public key
cert_file = "/some/path/to/cert.pem"
# Path to private key
key_file = "/some/path/to/key.pem"
client_cert = (cert_file, key_file)

# CCP query parameters
query_params = { "Safe": "<SAFE_NAME>", "Object": "<ACCOUNT_NAME>", "AppId": "<APP_ID>" }

# Safe name to query
safe_name = "Servers"

# Set inital http header
headers = {'Content-Type': 'application/json'}

# These likely will be the same but some do run a stand alone server for CCP.
ccp_url = "https://cyberark.lab/AIMWebService/api/Accounts"
pvwa_url = "https://cyberark.lab"

# Function to pull creds from CyberArk via the CCP and return the raw response
def get_creds():
    print("Getting creds for API user...", end="")
    url = ccp_url

    response = requests.get(url, headers=headers, params=query_params, cert=client_cert, verify=False)
    print("Done")

    return response.text

# Function to log into the CyberArk PAS API and return the auth token in a usable format
def api_login(user, password):
    print("Logging into API...", end="")
    url = pvwa_url + "/PasswordVault/API/Auth/CyberArk/Logon"

    payload = json.dumps({
        "username": user,
        "password": password
    })

    response = requests.post(url, headers=headers, data=payload, verify=False)
    print("Done")

    return response.text.strip('\"')

# Function to logoff the CyberArk PAS API
def api_logoff():
    print("Logging off API...", end="")
    url = pvwa_url + "/PasswordVault/API/Auth/Logoff"

    response = requests.post(url, headers=headers, verify=False)
    print("Done")

# Function to get 5 Safe names from CyberArk PAS and return the raw response
def get_safes():
    print("Getting 5 Safes...", end="")
    url = pvwa_url + "/PasswordVault/api/Safes?limit=5"

    response = requests.get(url, headers=headers, verify=False)
    print("Done")
    
    return json.loads(response.text)

# Call the get_creds function and set var with the result
creds = json.loads(get_creds())

# Call the api_login function and set var with the result
token = api_login(creds["UserName"], creds["Content"])

# Add the auth token to the headers for API requests
headers = { 'Authorization': token, 'Content-Type': 'application/json' }

# Get some Safes and set the var with the result
safes = get_safes()

# Loop through the Safes and print them to console
for safe in safes["value"]:
    print(json.dumps(safe, indent=4))

# Logoff the CyberArk PAS API
api_logoff()