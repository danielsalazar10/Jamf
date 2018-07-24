# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 17:19:59 2018
@author: Daniel
"""
import requests
import sys
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
    # Testing functions using Oxford Dictionary
    OX = 5

# Input:
#   1) api is an Enum of API
# Process:
#   This opens the config file for the corresponding API
# Output:
#   Returns the tree structure
def getConfigData(api):
    config = ['JSScredentials.json',
              'ODcredentials.json',
              'SNcredentials.json',
              'BFcredentials.json',
              'credentials.json'
             ]
    try:
        with open(config[api.value]) as data_file:
            return json.load(data_file)
    except:
        sys.exc_info()[0]

# Input:
#   cfg_data is the list which contains the URL, 
# Process:
#   This will loop through each of the cfg_data in order of the Enum.
#   It will extract the username and password from the cfg_data and use that to request authentication.
# Output:
#   auth is a list of authentications
def getAuth(cfg_data):
    try:
        return requests.auth.HTTPBasicAuth(cfg_data["credentials"]["username"],cfg_data["credentials"]["password"])
    except:
        sys.exc_info()[0]

# Input:
#   1) url is the base URL for the API
#   2) auth is the specific authentication data for the API
#   3) json is a switch for determining which to decode the data as
#   4) method is for the API call
#   5) head is for the API call
# Process:
#   This tries to get the API data and either decodes it as JSON or XML.
#   If it fails, it will halt the script and print out the reason why.
# Output:
#   returns decoded JSON data
def get(url,auth,method='mobiledevices',head={"Accept": "application/json"}):
    try:
        r = requests.get(url=(url + method), heading=head, auth=auth)
        if r.status_code != 200:
            r.raise_for_status()
        return r
    except:
        sys.exc_info()[0]
        
# Input:
#   1) api is one of the API Enums
#   2) method is what goes after the url, example: '/computerapplicationusage/id/%s/%s_%s'
# Process
#   This gets the configuration data
#   Then it authorizes using the username and password
#   Finally it gets the API response using a GET request
# Output:
#   response is the text version of the API call;JSON/XML data
def getResponse(api, method):
    cfg_data = getConfigData(api)
    auth = getAuth(cfg_data)
    return get(cfg_data["credentials"]["url"], auth, method)
