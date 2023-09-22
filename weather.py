from Bot_Functions import places
from dotenv import load_dotenv
import os
import requests
import json

def find_weather(location, units):
    load_dotenv()
    api_key = os.getenv('WEATHER_TOKEN')
    location = places.get_location(location)
    lat = location[0]
    lon = location[1]
    if location == 'invalid':
        return 'Invalid location'
    base_url = 'https://api.openweathermap.org/data/2.5/weather?'

    complete_url = base_url + 'lat=' + str(lat) + '&lon=' + str(lon) + '&appid=' + api_key + '&units='+ units

    response = requests.get(complete_url)
    report = response.json()
    if units == 'imperial':
        return ("temperature: " + str(report['main']['temp'])+ ' °F' +'\n'+
            "feels like: " + str(report['main']['feels_like'])+ ' °F' +'\n'+
            "minimum temp: " + str(report['main']['temp_min'])+ ' °F' +'\n'+
            "maximum temp: " + str(report['main']['temp_max'])+ ' °F')
    if units == 'metric':
        return ("temperature: " + str(report['main']['temp'])+ ' °C' +'\n'+
            "feels like: " + str(report['main']['feels_like'])+ ' °C' +'\n'+
            "minimum temp: " + str(report['main']['temp_min'])+ ' °C' +'\n'+
            "maximum temp: " + str(report['main']['temp_max'])+ ' °C')
    if units == 'standard':
        return ("temperature: " + str(report['main']['temp'])+ ' K' +'\n'+
            "feels like: " + str(report['main']['feels_like'])+ ' K' +'\n'+
            "minimum temp: " + str(report['main']['temp_min'])+ ' K' +'\n'+
            "maximum temp: " + str(report['main']['temp_max'])+ ' K')
    
