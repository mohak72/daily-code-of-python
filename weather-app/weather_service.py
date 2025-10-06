import os
import requests
from datetime import datetime
from dotenv import load_dotenv

class WeatherService:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        self.weather_url = "http://api.openweathermap.org/data/2.5/weather"
        self.forecast_url = "http://api.openweathermap.org/data/2.5/forecast"
        self.icon_url = "http://openweathermap.org/img/wn/{}@2x.png"
        
        if not self.api_key:
            raise ValueError("API key not found. Please set OPENWEATHER_API_KEY in .env file")

    def get_weather(self, city, units="metric"):
        """Get current weather data for a city."""
        try:
            params = {
                "q": city,
                "appid": self.api_key,
                "units": units
            }
            response = requests.get(self.weather_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            temp_unit = "C" if units == "metric" else "F"
            speed_unit = "m/s" if units == "metric" else "mph"
            
            return {
                "temperature": round(data["main"]["temp"], 1),
                "feels_like": round(data["main"]["feels_like"], 1),
                "humidity": data["main"]["humidity"],
                "description": data["weather"][0]["description"].capitalize(),
                "wind_speed": data["wind"]["speed"],
                "city": data["name"],
                "country": data["sys"]["country"],
                "icon_code": data["weather"][0]["icon"],
                "icon_url": self.icon_url.format(data["weather"][0]["icon"]),
                "temp_unit": temp_unit,
                "speed_unit": speed_unit
            }
        except requests.RequestException as e:
            raise ConnectionError(f"Failed to fetch weather data: {str(e)}")
        except (KeyError, ValueError) as e:
            raise ValueError(f"Failed to parse weather data: {str(e)}")

    def get_forecast(self, city, units="metric"):
        """Get 5-day forecast data for a city."""
        try:
            params = {
                "q": city,
                "appid": self.api_key,
                "units": units
            }
            response = requests.get(self.forecast_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            temp_unit = "C" if units == "metric" else "F"
            forecasts = []
            
            # Group forecasts by day (using 12:00 as representative time)
            daily_forecasts = {}
            for item in data["list"]:
                dt = datetime.fromtimestamp(item["dt"])
                if dt.hour == 12:  # Noon forecasts
                    daily_forecasts[dt.date()] = {
                        "date": dt.strftime("%Y-%m-%d"),
                        "day": dt.strftime("%A"),
                        "temperature": round(item["main"]["temp"], 1),
                        "description": item["weather"][0]["description"].capitalize(),
                        "icon_code": item["weather"][0]["icon"],
                        "icon_url": self.icon_url.format(item["weather"][0]["icon"]),
                        "temp_unit": temp_unit
                    }
            
            # Convert to list and sort by date
            forecasts = list(daily_forecasts.values())
            return forecasts[:5]  # Return 5 days of forecast
            
        except requests.RequestException as e:
            raise ConnectionError(f"Failed to fetch forecast data: {str(e)}")
        except (KeyError, ValueError) as e:
            raise ValueError(f"Failed to parse forecast data: {str(e)}")
