
import time
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import find_cheapest_flight
import datetime as dt
from notification_manager import NotificationManager

today=dt.datetime.now()
tomorrow=today+dt.timedelta(days=1)
next_sixmonths=tomorrow+dt.timedelta(days=(6*30))
ORIGIN_AIRPORT="BOG"

data_manager=DataManager()
sheet_data=data_manager.get_destination_data()
flight_search=FlightSearch()


for item_dict in sheet_data:
    if item_dict["iataCode"] == "":
        city_name=item_dict["city"]
        item_dict["iataCode"]=flight_search.get_destination_code(city_name)
        time.sleep(2)
        
        
        
data_manager.sheety_data=sheet_data
data_manager.updating_iata()


tomorrow_formatted=tomorrow.strftime("%Y-%m-%d")
next_sixmonths_formatted=next_sixmonths.strftime("%Y-%m-%d")



for destination in sheet_data:
    current_price=destination["lowestPrice"]
    origin_airport=ORIGIN_AIRPORT
    destination_airport=destination["iataCode"]
    out_date=tomorrow_formatted
    return_date=next_sixmonths_formatted
    flights=flight_search.check_flights(origin_airport,destination_airport,out_date,return_date)
    cheapest_flight = find_cheapest_flight(flights)
    
    if cheapest_flight.price != "N/A" and cheapest_flight.price <current_price:
        print(f"Lower price flight found to {destination['city']}!")
        email=NotificationManager()
        email.send_notification(cheapest_flight.price,cheapest_flight.origin_airport,cheapest_flight.destination_airport,cheapest_flight.out_date,cheapest_flight.return_date)
    
