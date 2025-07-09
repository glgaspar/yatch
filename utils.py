import sys
import requests
import os
import json

def api(method:str, path, data={})->dict:
    url = os.getenv('API_URL')+path
    
    params = {
        "key": os.getenv("API_KEY"),
        "token": os.getenv("API_TOKEN")
    }
    
    try:
        response = requests.request(method, url, params=params, data=data)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return sys.exit()

    try:
        json_data = response.json()
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return sys.exit()
    
    return json_data