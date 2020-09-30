import unittest
from api_handler import ApiHandler


class TestFuelApi(unittest.TestCase):
    def test_accessToken(self):
        ah = ApiHandler()
        result = ah.get_accessToken()
        self.assertIsInstance(result, str, msg="not valid access token.")

        result = len(ah.get_accessToken())
        self.assertEqual(result, 28, msg="access token length is not equal to 28.")