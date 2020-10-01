import requests
import time
import credentials
import uuid
import csv
import json
import os
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
        main_dir = os.path.dirname(__file__)
        suburbs_csv = f"{main_dir}/suburbs.csv"
        with open(suburbs_csv, "r") as f:
            lines = csv.reader(f)
            for line in lines:
                if line[1].lower() == suburb.lower() and line[4].strip() == "Delivery Area":
                    return line[0]

    def load_ref_data(self):
        main_dir = os.path.dirname(__file__)
        ref_data_json = f"{main_dir}/ref_data.json"
        with open(ref_data_json, 'r') as f:
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
        r = response.json()
        if 'errorDetails' in r.keys():
            print(r['errorDetails']['message'])
            print('Trying Local Database (Updated Nightly)')
            main_dir = os.path.dirname(__file__)
            fuel_json = f"{main_dir}/fuel_prices.json"
            data = {'prices': []}
            with open(fuel_json, "r") as f:
                r = json.load(f)
                for i in r['prices']:
                    if i['stationcode'] == station_code:
                        data['prices'].append(i)
            return data
        else:
            return r


    def stations_with_fuel_types(self, postcode):
        stations = self.get_stations(postcode)[:5]
        for station in stations:
            fuel_types = self.fuel_prices_single_station(station.code)
            # if 'errorDetails' in fuel_types.keys():
            #     print('This is an app that uses FREE API account from NSW government.')
            #     print('Limit is 5 API call per minute.')
            #     print(fuel_types['errorDetails']['message'])
            #     print('Waiting for a minute...')
            #     time.sleep(60)
            #     fuel_types = self.fuel_prices_single_station(station.code)
            for item in fuel_types["prices"]:
                fuel = Fuel(item["fueltype"], self.get_fuel_name(item["fueltype"]), item["price"])
                station.add_fuel_type(fuel)
        return stations

