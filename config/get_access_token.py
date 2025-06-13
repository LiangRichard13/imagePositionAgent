import requests
import json


secret_key="LVXR3JgAfsuej0RBZEq6o7EHDeU4XN1Q"
api_key="40vmdViIfPtjfbhztwoxZSuR"
token_url="https://aip.baidubce.com/oauth/2.0/token"

def main():
        
    url = f"{token_url}?grant_type=client_credentials&client_id={api_key}&client_secret={secret_key}"
    
    payload = ""
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    
    print(response.text)
    

if __name__ == '__main__':
    main()