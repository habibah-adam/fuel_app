import requests
import credentials
import uuid
import csv
import json
from pprint import pprint
from station import Station
from fuel import Fuel
from datetime import datetime
from datetime import timedelta




class ApiHandler:

    def __init__(self):

        self.base_url = "https://api.onegov.nsw.gov.au"
        self.access_token_url = "/oauth/client_credential/accesstoken?grant_type=client_credentials"
        self.ref_url = "/FuelCheckRefData/v1/fuel/lovs"
        self.price_url = "/FuelPriceCheck/v1/fuel/prices/station/"
        self.api_headers = {
            "Authorization":credentials.Authorization
        }

    @classmethod
    def get_uuid(cls):
        return str(uuid.uuid4())
    
    @classmethod
    def get_timestamp(cls, days=0):
        current_time = datetime.now() - timedelta(days)
        str_current_time = current_time.strftime("%d/%m/%Y %I:%M:%S %p")
        return str_current_time
  
    def get_accessToken(self):
        response = requests.get(f"{self.base_url}{self.access_token_url}", headers=self.api_headers)
        access_token = response.json()["access_token"]
        return access_token

    # def get_reference_data(self):
    #     response = requests.get(f"{self.base_url}{self.ref_url}", \
    #                         headers={"Authorization": f"Bearer {self.get_accessToken()}", \
    #                                  "apikey": credentials.api_key, \
    #                                  "Content-Type": "application/json", \
    #                                  "transactionid": ApiHandler.get_uuid(), \
    #                                  "requesttimestamp": ApiHandler.get_timestamp(), \
    #                                  "if-modified-since": ApiHandler.get_timestamp(365*5)})
    #     with open("ref_data.json", "w") as f:
    #         f.write(response.text)
        

    def get_postcode(self, suburb):
        with open("suburbs.csv") as f:
            lines = csv.reader(f)
            for line in lines:
                if line[1].lower() == suburb.lower() and line[4].strip() == "Delivery Area":
                    return line[0]

    def load_ref_data(self):
        with open("ref_data.json") as f:
            fuel_data = json.load(f)
        return fuel_data

    def get_stations(self, postcode):
        stations = []
        fuel_data = self.load_ref_data()
        for item in fuel_data["stations"]["items"]:
            if item["address"].endswith(f"{postcode}"):
                station = Station(item["brand"], item["name"], item["code"], item["address"])
                stations.append(station)
        return stations

    def get_fuel_name(self, fuel_code):
        fuel_data = self.load_ref_data()
        for item in fuel_data["fueltypes"]["items"]:
            if item["code"] == fuel_code:
                return item["name"]

    def fuel_prices_single_station(self, station_code):
        response = requests.get(f"{self.base_url}{self.price_url}{station_code}", \
            headers={
                "Authorization": f"Bearer {self.get_accessToken()}", \
                "apikey": credentials.api_key, \
                "Content-Type": "application/json", \
                "transactionid": ApiHandler.get_uuid(), \
                "requesttimestamp": ApiHandler.get_timestamp()
            })
        return response.json()

    def stations_with_fuel_types(self, postcode):
        stations = self.get_stations(postcode)[:5]
        for station in stations:
            print(station.name, id(station), id(station.fuel_types))
            fuel_types = self.fuel_prices_single_station(station.code)
            for item in fuel_types["prices"]:
                fuel = Fuel(item["fueltype"], self.get_fuel_name(item["fueltype"]), item["price"])
                station.add_fuel_type(fuel)
        return stations

ah = ApiHandler()
s = ah.stations_with_fuel_types(2194)

for i in s:
    pprint(i.fuel_types)




