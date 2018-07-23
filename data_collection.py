from enum import Enum
class API(Enum):
    # Jamf: JSS REST API
    JSS = 1
    # MSCCM: System Center Orchestrator OData REST API
    OD = 2
    # ServiceNow: Scripted REST API
    SN = 3
    # BigFix: BigFix REST API
    BF = 4

# Input:
#   1) cfg_file is a filename
# Process:
#   This will try to open the configuration file
#   Then it will try to load the cfg_data from the JSON file
#   If it fails, the script will hault with a detail message
# Output:
#   cfg_data is the list which represents the URL/username/password
def readConfig(cfg_file):
    try:
        with open(cfg_file) as data_file:
            cfg_data = json.load(data_file)
            return cfg_data
    except:
        sys.exc_info()[0]

# Input:
#   1) api is a number form 1-4; representing one of the API Enums
# Process:
#   Switch on a number, returning a cfg_filename
# Output:
#   returns cfg_file for use in
def getConfigFile(api):
    return {
        1: '../JSScredentials.json',
        2: '../ODcredentials.json',
        3: '../SNcredentials.json',
        4: '../BFcredentials.json'
    }[api]

# Process:
#   This will loop through each of the values in the Enum: 1-4.
#   Those numbers are passed into getConfigFile() to get filenames.
#   Those filenames are passed into readConfig() to get the data as a list.
#   Those lists are appended to config and returned.
# Output:
#   A list of cfg_data for use in setAuth()
def getConfigData():
    # Read configuration files for each API
    cfg_data = []
    for api in API:
        cfg_data.append(readConfig(getConfigFile(api.value)))
    return cfg_data

# Input:
#   1) cfg_data is a list of cfg_data
# Process:
#   This will loop through each of the cfg_data.
#   It will extract the username and password from the cfg_data and use that to request authentication.
# Output:
#   1) auth is a list of authentications, for use as an argument for requests.get()
def setAuth(cfg_data):
    auth = []
    for data in cfg_data:
        try:
            auth.append(requests.auth.HTTPBasicAuth(data["credentials"]["username"],data["credentials"]["password"]))
        except:
            e = sys.exc_info[0]
    return auth
