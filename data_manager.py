import requests
import os
from dotenv import load_dotenv
from pprint import pprint
load_dotenv()

class DataManager:
   
    def __init__(self):
        self.sheety_enp=os.getenv("SHEETY_ENP")
        self.sheety_token=os.getenv("SHEETY_TOKEN")
        self.headers={
            "Authorization":self.sheety_token
        }
        self.sheety_data={}
    
        
    def get_destination_data(self):
        
        self.sheety_get_response=requests.get(url=self.sheety_enp,headers=self.headers)
        self.sheety_get_response.raise_for_status()
        self.sheety_data=self.sheety_get_response.json()['prices']
        return self.sheety_data
    def updating_iata(self):
        
        for city in self.sheety_data:
            parameters={
                "price":{
                    "iataCode":city["iataCode"]
                }
            }
            sheety_put_response=requests.put(url=f"{self.sheety_enp}/{city["id"]}",headers=self.headers, json=parameters)
            