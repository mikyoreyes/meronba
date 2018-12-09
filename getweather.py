# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 16:31:51 2018

@author: raymond.d.abargos
"""
import tornado.ioloop
import tornado.web
import pyowm
import json
import googlemaps


class MainHandler(tornado.web.RequestHandler):
    
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Origin, Content-Type, Accept, Authorization, X-Request-With")
        self.set_header("Access-Control-Allow-Methods", "GET, POST, DELETE, PUT, OPTIONS")
        self.set_header("Access-Control-Allow-Credentials", "true")
        self.set_header("Content-Type", 'application/json')

    def options(self, *args):
        self.set_status(200)
        self.finish()
        
    def get(self):
        json_response = {
            "success": True,
            "message": "Hello world!"
        }
        self.write(json_response)
        self.finish()

    def post(self):
        json_request = tornado.escape.json_decode(self.request.body)
        latitude = json_request['latitude']
        longitude = json_request['longitude']
        weather, city = get_weather(latitude, longitude)
        json_response = {
            "success": True,
            "weather": weather,
            "city": city
        }
        self.write(json.dumps(json_response))
        self.finish()
        

def get_weather(latitude, longitude):
    OWM_API_KEY = '38ee6f2c3acb748ce95d5ab5cca6b25f'
    owm = pyowm.OWM(OWM_API_KEY)  # You MUST provide a valid API key
    
    # Search for current weather
    city = get_city(latitude, longitude)
    location = city + ', philippines'
    observation = owm.weather_at_place(location.lower())
    w = observation.get_weather()
    weather = w.get_status()
    
    return weather, city

def get_city(latitude, longitude):
    api_key = "AIzaSyCgQTuzNIRJEsyEzR0dGGU6uPBtmAKHZxg"
    gmaps = googlemaps.Client(key=api_key)
    reverse_geocode_result = gmaps.reverse_geocode((latitude, longitude))
    city = reverse_geocode_result[0]['address_components'][2]['long_name']
    return city

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler)
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(443)
    print("Weather service listening on port 443...")
    tornado.ioloop.IOLoop.current().start()
