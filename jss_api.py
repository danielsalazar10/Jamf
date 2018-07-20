# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 17:19:59 2018

@author: vu7972
Inspired by sreyemnayr JSSAPI:
https://github.com/sreyemnayr/jamf_pro_api/blob/master/jssapi/jssapi.py
"""
import requests
import sys
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning

class JSSAPI:
    def __init__(self,
                 url='',
                 head={"Accept": "application/json"},
                 user='', pwd=''):
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        self.url = url + '/JSSResource/'
        self.head = head
        self.auth = requests.auth.HTTPBasicAuth(user, pwd)
        self.r = requests.Response
        self.e = sys.exc_info()[0]
        
    def get(self, method='mobiledevices'):
        try:
            self.r = requests.get(url=(self.url + method), headers=self.head, auth=self.auth)
            if self.r.status_code != 200:
                self.r.raise_for_status()
            # Convert to JSON
            json = self.r.json()
            return next(iter(json.values()))
        except:
            self.e = sys.exec_info[0]
        return []
        
    def set_auth(self, cfg_file='../credentials.json'):
        try:
            with open(cfg_file) as data_file:
                data = json.load(data_file)
                self.auth = requests.auth.HTTPBasicAuth(data["credentials"]["username"],
                                                        data["credentials"]["password"])
        except:
            self.e = sys.exc_info[0]
    
    def queryBFviaRelevance(self, rVance):
        self.set_auth()
        self.get('/api/login')
        self.get('/api/query?relevance=' + rVance)
    
