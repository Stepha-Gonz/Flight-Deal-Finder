import requests
import os
from dotenv import load_dotenv
load_dotenv()

TOKEN_ENP=os.getenv("TOKEN_END_AMA")
END_AMA=os.getenv("END_AMA")
TOKEN_AMA=os.getenv("TOKEN_AMA")
FLIGHTS_ENP=os.getenv("FLIGHTS_ENP")
class FlightSearch:
    
    def __init__(self) :
        self.apikey=os.getenv("APIKEY_AMA")
        self.apisec=os.getenv("APISEC_AMA")
        self.tokenama=self.get_new_token()
        
        
    def get_new_token(self):
        header={
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        parameters={
            'grant_type': 'client_credentials',
            'client_id': self.apikey,
            'client_secret': self.apisec
        }
        ama_post_response=requests.post(url=TOKEN_ENP,headers=header,data=parameters)
        return ama_post_response.json()['access_token']
    def get_destination_code(self,city_name):
        
        header_iata={
            "Authorization": f"Bearer {self.tokenama}"
        }
        query ={
            "keyword":city_name,
            "max": "2",
            "include": "AIRPORTS",
        }
        response=requests.get(url=END_AMA,headers=header_iata,params=query )
        try:
            data=response.json()["data"][0]["iataCode"]
        except IndexError:
            print(f"IndexError: No airport code found for {city_name}.")
            return "N/A"
        except KeyError:
            print(f"KeyError: No airport code found for {city_name}.")
            return "Not Found"
        
        return data
    
    def check_flights(self,origin_city_code, destination_city_code, from_time, to_time):
        headers={
            "Authorization": f"Bearer {self.tokenama}"
        }
        
        parameters={
            "originLocationCode":origin_city_code,
            "destinationLocationCode":destination_city_code,
            "departureDate":from_time,
            "returnDate":to_time,
            "adults":1,
            "nonStop":"true",
            "currencyCode": "USD",
            "max":10
        }
        
        response_flights=requests.get(url=FLIGHTS_ENP,headers=headers,params=parameters)
        
        if response_flights.status_code != 200:  # Cambiar a verificación correcta del código
            print(f"check_flights() response code: {response_flights.status_code}")
            print("Response data:", response_flights.json()) 
            return None

        return response_flights.json()