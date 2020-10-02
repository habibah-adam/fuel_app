import unittest
from api_handler import ApiHandler


class TestFuelApi(unittest.TestCase):
    def test_accessToken(self):
        ah = ApiHandler()
        result = ah.get_accessToken()
        self.assertIsInstance(result, str, msg="not valid access token.")
        self.assertEqual(len(result), 28, msg="access token length is not equal to 28.")


    def test_postCode(self):
        ah = ApiHandler()
        result = ah.get_postcode("liverpool")
        self.assertTrue(result.isnumeric(), msg="postcode is not numeric." )
        self.assertEqual(len(result), 4, msg="postcode length is not equal to 4.")

        result = ah.get_postcode("urumqi")
        self.assertIsNone(result, msg="for wrong suburb should return None.")

    def test_fuelName(self):
        ah = ApiHandler()
        fuel_names = ["Unleaded 91", "Ethanol 94", "Premium 95","Premium 98", "Diesel"]
        result1 = ah.get_fuel_name("E10")
        result2 = ah.get_fuel_name("U91")
        result3 = ah.get_fuel_name("DL")
        result4 = ah.get_fuel_name("P98")
        result5 = ah.get_fuel_name("P93")
        self.assertIn(result1, fuel_names, msg=f"{result1} not in {fuel_names}")
        self.assertIn(result2, fuel_names, msg=f"{result2} not in {fuel_names}")
        self.assertIn(result3, fuel_names, msg=f"{result3} not in {fuel_names}")
        self.assertIn(result4, fuel_names, msg=f"{result4} not in {fuel_names}")
        self.assertIsNone(result5, msg=f"{result5} is not None.")

    def test_getStations(self):
        ah = ApiHandler()
        result1 = ah.get_stations("2194")
        result2 = ah.get_stations("830000")
        self.assertIsInstance(result1, list, msg="result is not list.")
        self.assertEqual(result2, [], msg="for wrong postcode should return empty list.")

        

        
