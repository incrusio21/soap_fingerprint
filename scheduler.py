import json
import os

import requests
import yaml

from bs4 import BeautifulSoup
from constants.utils import as_json, find_data_file, set_args

class FingerprintSOAP(object):
    def __init__(self, ip="192.168.1.210", port=80, com_key="0", hostname="", api_key="", api_secret=""):
        self.url = f'http://{ip}/iWsService'
        self.port = port
        self.com_key = com_key
        self.timeout = 1
        self.headers = {'Content-Type': 'text/xml'}    
        
        self.hostname = hostname
        self.api_key = api_key
        self.api_secret = api_secret

    def get_headers(self):
        return {
            'Authorization': f'token {self.api_key}:{self.api_secret}',
            'Content-Type': 'application/json',
        }

    def insert_to_fingerprint_log(self, data):
        # kirim data ke erpnext
        response = requests.request(
            "POST", 
            f"{self.hostname}/api/resource/Fingerprint Log", 
            headers=self.get_headers(), 
            data=json.dumps({"data": data})
        )

        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            return
        
    def get_log_data(self):
        # load soap dari fingerprint
        body = f"""<GetAttLog><ArgComKey xsi:type="xsd:integer">{self.com_key}</ArgComKey><Arg><PIN xsi:type="xsd:integer">All</PIN></Arg></GetAttLog>"""
        request = requests.post(self.url, data=body, headers=self.headers)
        if request.status_code != 200:
            print(f"Error: {request.status_code} - {request.text}")
            return
        
        if not request.text:
            return
        
        # scriping data xml
        soup = BeautifulSoup(request.text, "xml")
        log_list = []
        for row in soup.find_all("Row"):
            log_list.append({
                "pin": row.find("PIN").find(string=True),
                "date_time": row.find("DateTime").find(string=True),
                "verified": row.find("Verified").find(string=True),
                "status": row.find("Status").find(string=True),
                "workcode": row.find("WorkCode").find(string=True)
            })

        if not log_list:
            return

        # insert data ke erpnext
        self.insert_to_fingerprint_log({
            "type": "Import Data Log",
            "data": as_json({"data": log_list})
        })        

def get_fp_soap():
    stream = find_data_file(os.path.dirname(__file__), "setting.yaml", True)
    try:
        setting = yaml.safe_load(stream)
        args = {}
        set_args(args, setting.get("SOAP", {}))
        set_args(args, setting.get("ERPNext", {}))
        
        fp = FingerprintSOAP(**args)
        return fp
    except yaml.YAMLError as exc:
        print(exc)