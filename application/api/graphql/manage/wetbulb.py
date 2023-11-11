import decimal
import math
import pgeocode as pgeocode
import requests

from application.api.graphql.schema.wetbulb_schema import WetbulbSchema


class Wetbulb:
    async def calculate_wetbulb(self, relative_humidity: decimal, temperature: decimal) -> decimal:
        wetbulb = temperature * math.atan(0.152*math.pow((relative_humidity+8.3136), .5)) + \
            math.atan(temperature + relative_humidity) - math.atan(relative_humidity - 1.6763) + \
            0.00391838 * math.pow(relative_humidity, (3/2)) * math.atan(0.0231 * relative_humidity) - 4.686
        return wetbulb

    async def get_coordinates(self, postal_code: str):

        nomi = pgeocode.Nominatim('us')
        query = nomi.query_postal_code(postal_code)

        data = {
            "latitude": query["latitude"],
            "longitude": query["longitude"]
        }
        return data

    async def get_wetbulb(self, postal_code: str) -> WetbulbSchema:
        coordinates = await self.get_coordinates(postal_code=postal_code)
        weather = await self.get_weather(coordinates)

        relative_humidity = weather['properties']['periods'][0]['relativeHumidity']['value']
        temperature = weather['properties']['periods'][0]['temperature']

        print(f'relative_humidity: {relative_humidity}')
        print(f'temperature: {temperature}')
        celcius_temperature = await self.get_celcius(temperature)
        wetbulb = self.calculate_wetbulb(relative_humidity, celcius_temperature)

        wetbulb_schema = WetbulbSchema(
            wetbulb=wetbulb
        )
        return wetbulb_schema

    async def get_weather(self, coordinates: dict) -> dict:
        url = f'https://api.weather.gov/points/{coordinates["latitude"]},{coordinates["longitude"]}'
        headers = {'Content-Type': 'application/json'}
        coordinate_response = requests.get(url, headers=headers)
        coordinate_response_json = coordinate_response.json()
        weather_url = coordinate_response_json['properties']['forecast']

        weather_response = requests.get(weather_url, headers=headers)
        weather_response_json = weather_response.json()

        return weather_response_json

    async def get_celcius(self, fahrenheit_temperature):
        print(f'F: {fahrenheit_temperature}')
        celcius = ((fahrenheit_temperature - 32)*5)/9
        print(f'C: {celcius}')
        return celcius
