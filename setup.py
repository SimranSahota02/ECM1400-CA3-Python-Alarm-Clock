import json
import logging
import requests

import pyttsx3
from uk_covid19 import Cov19API

import alarm_handler

def setup():
    """The setup function returns two lists of dictionaries. The first return is the 
    news/weather/covid brief. The second return is the alarms. This function is called in the 
    main function."""
    return construct_brief(), construct_alarms()

def get_config(file="config.txt"):
    """This function returns the api keys for the news and weather modules, alongside the name
    of the city to be used in the function. The default parameter should be called in every
    instance."""
    with open(file) as config_file:
        config_data = json.load(config_file)
        
        return config_data["news_api_key"], config_data["open_weather_api_key"], config_data["city"]

    config_file.close()

def api_request_setup(news_key,weather_key, city):
    """This function takes input api keys and city name to construct the api requests as strings.
    It then returns these three strings to be used to request data from the APIs."""

    #construct news api string
    news_req_str_top = ("http://newsapi.org/v2/top-headlines?" + "country=gb&"
    + "apiKey=" + news_key)

    #construct weather api string
    weather_req_str = ("http://api.openweathermap.org/data/2.5/weather?q=" + city 
    + "&appid=" + weather_key)

    #construct covid api string
    covid_req_str = ("https://api.coronavirus.data.gov.uk/v1/data?filters=areaName=" + city.lower()
    + '&structure={"date":"date","newCases":"newCasesByPublishDate","newDeaths":'
    + '"newDeathsByDeathDate"}')

    return news_req_str_top, weather_req_str, covid_req_str

def get_new_news(news_req) -> list:
    """Function get_new_news takes string news_req and uses it to make a request to the news api
    newsapi. It returns a list of stories. The stories are the most recent top 5 uk stories.Each 
    story is a dictionary containing the news story title and the url as the content."""
    try:
        top_news = requests.get(news_req)
        top_news_articles = top_news.json()["articles"]
        stories_list = []
        new_news = []
        for i in range(0,5):
            story = {}
            stories_list.append(top_news_articles[i])
            story["title"] = (stories_list[i])["title"] 
            story["content"] = (stories_list[i])["url"]
            new_news.append(story)

        return new_news
    except:
        logging.error("Detected failed API request in get_new_news method. Refer to README.txt."
        + " Potential error in request or invalid API key.")

def get_new_weather(weather_req, city) -> dict:
    """Function get_new_weather takes strings weather_req and city uses them to make a request to
    weather api openweatherapi. It returns a dictionary. The dictionary has a title that states
    the location and purpose of the weather notification. It also has content that contains the
    data about the weather in the given city."""
    try:
        local_weather = requests.get(weather_req)
        local_weather_data = local_weather.json()
    
        new_weather = {}
        new_weather["title"] = "Weather report for " + city
        
        #The weather values are converted from kelvin to degrees celsius and rounded to 2d.p.
        new_weather["content"] = ((((local_weather_data["weather"])[0])["description"]) + ", temperature "
        + str(round(float(((local_weather_data["main"])["temp"])) - 273.15, 2)) + "°C. Feels like "
        + str(round(float(((local_weather_data["main"])["feels_like"])) 
        - 273.15, 2)) + ".")
    
        return new_weather
    except:
        logging.error("Detected failed API request in get_new_weather method. Refer to README.txt."
        + " Potential error in request or invalid API key.")

def get_new_covid(covid_req, city) -> dict:
    """Function get_new_covid takes strings covid_req and city and uses them to make a request to
    the uk.gov covid module api. It returns a dictionary that contains title stating location and
    purpose of the notification. The content value is a string concatenated from the data requests
    to the api."""
    try:
        covid_stats = requests.get(covid_req, city)
        new_covid = {}
        new_covid["title"] = "Covid report for " + city

        #the dictionary "data" within the dictionary covid_stats.json is accessed to return useable data
        new_covid["content"] = ("As of " + str(((covid_stats.json()["data"])[0])["date"]) 
        + " there have been " + str(((covid_stats.json()["data"])[0])["newCases"]) 
        + " new cases and " + str(((covid_stats.json()["data"])[0])["newDeaths"]) + " new deaths.")

        return new_covid
    except:
        logging.error("Detected failed API request in get_new_covid method. Refer to README.txt."
        + " Potential error in request or invalid API key.")

def assemble_brief(news_brief,weather_brief,covid_brief) -> list:
    """Function assemble_brief takes three input briefs and returns a single data structure that
    contains a list of dictionaries to be used as notifications with html template. weather_brief
    and covid_brief are appended to the list seperately of news_brief, as news_brief is a list of
    dictionaries rather than a dictionary of its own."""
    brief = [weather_brief,covid_brief]
    
    for i in news_brief:
        brief.append(i)

    return brief

def construct_brief() -> list:
    """This function coordinates the functions that request data from the apis and those that 
    format it to return a list of dictionaries. This function is called in the setup 
    function."""

    #Request data from APIs
    news_key, weather_key, city = get_config("config.txt")
    news_req, weather_req, covid_req = api_request_setup(news_key, weather_key, city)
    
    #Now compile obtained data 
    news_brief = get_new_news(news_req)
    weather_brief = get_new_weather(weather_req, city)
    covid_brief = get_new_covid(covid_req, city)
    formatted_brief = assemble_brief(news_brief,weather_brief,covid_brief)

    return formatted_brief

def construct_alarms() -> list:
    """This function returns a list of alarms as dictionaries. It calls functions from module 
    alarm_handler to do this. This function allows the setup function to retrieve alarm data 
    upon startup and is also called by other alarm setting functions to reset and format 
    alarms."""
    alarms = alarm_handler.get_alarms("log.log")
    formatted_alarms = alarm_handler.displayable_alarms(alarms)

    return formatted_alarms