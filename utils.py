import requests
import os
import json

def api(method:str, path, data=None)->dict:
    url = f"{os.getenv("API_URL")}{path}"
    params = {
        "key": os.getenv("API_KEY"),
        "token": os.getenv("API_TOKEN")
    }
    response = requests.request(method, url, params=params, data=data)
    
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return dict()

    try:
        json_data = response.json()
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return dict()
    
    return json_data