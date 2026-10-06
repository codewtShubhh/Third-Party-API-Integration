import os
import httpx
from dotenv import load_dotenv

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
WEATHER_API_URL = "https://api.weatherapi.com/v1/current.json"


async def get_weather(city):
    params = {
        "key": WEATHER_API_KEY,
        "q": city
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
               WEATHER_API_URL,
               params=params,
               timeout=10.0
            )

        if response.status_code != 200:
            return {
                "success": False,
                "message": "Unable to fetch weather data",
                "status_code": response.status_code
            }

        data = response.json()

        return {
            "success": True,
            "data": {
                "city": data["location"]["name"],
                "country": data["location"]["country"],
                "temperature_c": data["current"]["temp_c"],
                "condition": data["current"]["condition"]["text"],
                "humidity": data["current"]["humidity"],
                "wind_kph": data["current"]["wind_kph"]
            }
        }

    except httpx.RequestError:
        return {
            "success": False,
            "message": "Weather service is unavailable",
            "status_code": 503
        }