import requests
import credentials
import uuid
from datetime import datetime
from datetime import timedelta



class ApiHandler:

    def __init__(self):

        self.base_url = "https://api.onegov.nsw.gov.au"
        self.access_token_url = "/oauth/client_credential/accesstoken?grant_type=client_credentials"
        self.ref_url = "/FuelCheckRefData/v1/fuel/lovs"
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

    def get_reference_data(self):
        response = requests.get(f"{self.base_url}{self.ref_url}", \
                            headers={"Authorization": f"Bearer {self.get_accessToken()}", \
                                     "apikey": credentials.api_key, \
                                     "Content-Type": "application/json", \
                                     "transactionid": "uuid123413", \
                                     "requesttimestamp": ApiHandler.get_timestamp(), \
                                     "if-modified-since": ApiHandler.get_timestamp(365*5)})
        return response.json()

    def 

    


ah = ApiHandler()
print(ah.get_accessToken())
print(ah.get_reference_data())



