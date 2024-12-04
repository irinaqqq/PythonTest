import requests
import logging
from cachetools import TTLCache

logging.basicConfig(level=logging.INFO) 

API_KEY = "08f8b77ee32d7851eaedd170c3288ada"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

weather_cache = TTLCache(maxsize=100, ttl=600)

def fetch_weather(city: str):
    if city in weather_cache:
        logging.info(f"Returning cached weather data for {city}")
        return weather_cache[city]
    
    logging.info(f"Fetching new weather data for {city}")
    
    try:
        params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric"
        }
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        
        weather_data = parse_weather_response(response.json())

        weather_cache[city] = weather_data

        return weather_data

    except requests.exceptions.Timeout:
        logging.error(f"Error fetching weather data for {city}: Timeout")
        raise RuntimeError(f"Error fetching weather data for {city}: Timeout")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching weather data for {city}: {str(e)}")
        raise RuntimeError(f"Error fetching weather data for {city}: {str(e)}")

def parse_weather_response(data: dict):
    try:
        if "main" not in data or "temp" not in data["main"]:
            raise ValueError("Missing 'main' or 'temp' in the response data.")
        if "weather" not in data or not isinstance(data["weather"], list) or not data["weather"]:
            raise ValueError("Missing 'weather' field or invalid format.")
        
        return {
            "city": data.get("name", "Unknown"),
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"]
        }
    except (KeyError, IndexError) as e:
        logging.error(f"Unexpected response structure: {str(e)}")
        raise ValueError(f"Unexpected response structure: {str(e)}")
