from datetime import datetime
import requests
import unittest

from uk_covid19 import Cov19API

import main
import setup
import sched_handler
import alarm_handler
import notification_handler

class TestDateTime(unittest.TestCase):

    invalidstr = 121231

    #Test valid input returns correct datetime object
    def test_create_datetime_valid(self):
        self.assertTrue(datetime(2020,11,11,12,21,00)) == sched_handler.create_datetime_date("2020.11.11 12:21")

    #Test invalid input returns type error
    def test_create_datetime_invalid(self):
        self.assertRaises(TypeError, sched_handler.create_datetime_date, self.invalidstr)

class TestAPIReq(unittest.TestCase):
     
    #Obtain good test data from config file using setup functions
    def setup_api_requests(self):
        news_key, weather_key, city = setup.get_config("config.txt")
        newsreq, weatherreq, covidreq = setup.api_request_setup(news_key,weather_key, city)

        return newsreq, weatherreq, covidreq, city

    #Test news api valid request gets good response
    def test_news_api_valid(self):
        newsreq, weatherreq, covidreq, city = self.setup_api_requests()
        requested = requests.get(newsreq)
        self.assertEqual(requested.status_code,200)
    
    #Test weather api valid request gets good response
    def test_weather_api_valid(self):
        newsreq, weatherreq, covidreq, city = self.setup_api_requests()
        requested = requests.get(weatherreq)
        self.assertEqual(requested.status_code,200)

    #Test covid api valid request gets good response
    def test_covid_api_valid(self):
        newsreq, weatherreq, covidreq, city = self.setup_api_requests()
        requested = requests.get(covidreq, city)
        self.assertEqual(requested.status_code,200)

    #Test news api invalid request gets bad response
    def test_news_api_invalid(self):
        newsreq, weatherreq, covidreq, city = self.setup_api_requests()
        newsreq += "invalidstring"
        requested = requests.get(newsreq)
        self.assertNotEqual(requested.status_code,200)

    #Test weather api invalid request gets bad response
    def test_weather_api_invalid(self):
        newsreq, weatherreq, covidreq, city = self.setup_api_requests()
        weatherreq += "invalidstring"
        requested = requests.get(weatherreq)
        self.assertNotEqual(requested.status_code,200)

    #Test covid api invalid request gets bad response
    def test_covid_api_invalid(self):
        newsreq, weatherreq, covidreq, city = self.setup_api_requests()
        covidreq += "invalidstring"
        requested = requests.get(covidreq)
        self.assertNotEqual(requested.status_code,200)

if __name__ == "__main__":
    unittest.main()
