import requests
from findtemp_weather import findtemperature, findcreated_at
from pprint import pprint
from database_connection import cursor, connection
import json
import _thread
import random
from datetime import datetime

def findweather():
    number = random.uniform(0, 1)
    if (number <= 0.25):
     city="Ottawa"
     url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=58072d45ddf713df4b440b2afde4d2be&units=metric'.format(city)
     res = requests.get(url)
     data = res.json()
     temp = data['main']['temp']
     wind_speed = data['wind']['speed']
     feels_like = data['main']['feels_like']
     pressure = data['main']['pressure']
     humidity = data['main']['humidity']
     visibility = data['visibility']
     description = data['weather'][0]['description']

     return('Temperature : {} degree celcius'.format(temp), 'Wind Speed : {} m/s'.format(wind_speed), 'Description : {}'.format(description), 'Feels like : {}'.format(feels_like), 'Humidity : {}'.format(humidity), 'Pressure : {}'.format(pressure), 'Visibility : {}'.format(visibility),city )
    elif(number > 0.25 and number <=0.5):
        city = "Brampton"
        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=58072d45ddf713df4b440b2afde4d2be&units=metric'.format(
            city)
        res = requests.get(url)
        data = res.json()
        temp = data['main']['temp']
        wind_speed = data['wind']['speed']
        feels_like = data['main']['feels_like']
        pressure = data['main']['pressure']
        humidity = data['main']['humidity']
        visibility = data['visibility']
        description = data['weather'][0]['description']


        return ('Temperature : {} degree celcius'.format(temp), 'Wind Speed : {} m/s'.format(wind_speed),
                'Description : {}'.format(description), 'Feels like : {}'.format(feels_like),
                'Humidity : {}'.format(humidity), 'Pressure : {}'.format(pressure),
                'Visibility : {}'.format(visibility),city)

    elif (number > 0.5 and number <= 0.75):
        city = "Montreal"
        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=58072d45ddf713df4b440b2afde4d2be&units=metric'.format(
            city)
        res = requests.get(url)
        data = res.json()
        temp = data['main']['temp']
        wind_speed = data['wind']['speed']
        feels_like = data['main']['feels_like']
        pressure = data['main']['pressure']
        humidity = data['main']['humidity']
        visibility = data['visibility']
        description = data['weather'][0]['description']

        return ('Temperature : {} degree celcius'.format(temp), 'Wind Speed : {} m/s'.format(wind_speed),
                'Description : {}'.format(description), 'Feels like : {}'.format(feels_like),
                'Humidity : {}'.format(humidity), 'Pressure : {}'.format(pressure),
                'Visibility : {}'.format(visibility), city)
    else:
        city = "Vancouver"
        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=58072d45ddf713df4b440b2afde4d2be&units=metric'.format(city)
        res = requests.get(url)
        data = res.json()
        temp = data['main']['temp']
        wind_speed = data['wind']['speed']
        feels_like = data['main']['feels_like']
        pressure = data['main']['pressure']
        humidity = data['main']['humidity']
        visibility = data['visibility']
        description = data['weather'][0]['description']

        return ('Temperature : {} degree celcius'.format(temp), 'Wind Speed : {} m/s'.format(wind_speed),
                'Description : {}'.format(description), 'Feels like : {}'.format(feels_like),
                'Humidity : {}'.format(humidity), 'Pressure : {}'.format(pressure),
                'Visibility : {}'.format(visibility), city)


def weatherinfo(weatherdetails):
    Temperaturedetails = (weatherdetails[0].split(':'))[1]
    Windspeed = (weatherdetails[1].split(':'))[1]
    Description = (weatherdetails[2].split(':'))[1]
    Feelslike = (weatherdetails[3].split(':'))[1]
    Humidity = (weatherdetails[4].split(':'))[1]
    Pressure = (weatherdetails[5].split(':'))[1]
    Visibility =(weatherdetails[6].split(':'))[1]
    if(weatherdetails[7]=="Brampton"):
       direction="South to North"
    elif(weatherdetails[7]=="Ottawa"):
       direction = "North to South"
    elif(weatherdetails[7]=="Montreal"):
        direction = "East to West"
    else:
        direction="West to East"


    Temperature=findtemperature(Temperaturedetails)
    now = datetime.now()
    created_at = findcreated_at(now)
    postgres_insert_queryweather= """update public.project_weather set temperature= %s,humidity =%s,created_at=%s,created_time=%s, windspeed=%s,pressure=%s,"Visibility"=%s,feels_like=%s,description=%s where direction=%s"""
    record1_to_insert = (Temperature[0],Humidity,created_at, now, Windspeed, Pressure, Visibility, Feelslike, Description,direction)
    cursor.execute(postgres_insert_queryweather, record1_to_insert)
    connection.commit()
    count = cursor.rowcount

while True:
    weatherdetails = findweather()
    weatherinfo(weatherdetails)
