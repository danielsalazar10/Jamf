# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 17:19:59 2018
@author: Daniel
"""
import requests
import sys
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

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
#   cfg_file is a string representing the config file of the respective api
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
#   cfg_data is a list of URL/credentials
def getConfigData():
    cfg_data = []
    for api in API:
        cfg_data.append(readConfig(getConfigFile(api.value)))
    return cfg_data

# Process:
#   This will loop through each of the cfg_data in order of the Enum.
#   It will extract the username and password from the cfg_data and use that to request authentication.
# Output:
#   auth is a list of authentications
def getAuth(cfg_data):
    auth = []
    for data in cfg_data:
        try:
            auth.append(requests.auth.HTTPBasicAuth(data["credentials"]["username"],data["credentials"]["password"]))
        except:
            sys.exc_info()[0]
    return auth

# Input:
#   1) url is the base URL for the API
#   2) auth is the specific authentication data for the API
#   3) json is a switch for determining which to decode the data as
#   4) method is for the API call
#   5) head is for the API call
# Process:
#   This tries to get the API data and either decodes it as JSON or XML
# Output:
#   returns decoded JSON data
def get(url,auth,json,method='mobiledevices',head={"Accept": "application/json"}):
    try:
        r = requests.get(url=(url + method), heading=head, auth=auth)
        if r.status_code != 200:
            r.raise_for_status()
        if json:
            return r.json()
        else:
            return r.text()
    except:
        sys.exc_info()[0]

# Input:
#   1) api represents which API to get data for
#   2) cfg_data is a list of config URL/credentials
#   3) auth is a list of authenticated requests
# Process:
#   This goes down the list making API calls to the respective servers and putting them in a list
# Output:
#   returns a list, containing either JSON or XML decoded data
def getAPIData():
    all_api_data = []
    cfg_data = getConfigData()
    auth = getAuth()
    # Jamf: JSS REST API
    all_api_data.append(get(cfg_data[0]["credentials"]['url'],auth[0],True))
    # MSCCM: System Center Orchestrator OData REST API
    all_api_data.append(get(cfg_data[1]["credentials"]['url'],auth[1],True))
    # ServiceNow: Scripted REST API
    all_api_data.append(get(cfg_data[2]["credentials"]['url'],auth[2],True))
    # BigFix: BigFix REST API
    all_api_data.append(get(cfg_data[3]["credentials"]['url'],auth[3],False))
    return all_api_data
