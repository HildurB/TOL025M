import requests
import openmeteo_requests
from retry_requests import retry
import requests_cache


def get_location_info(place_string):
    """
    Retrieves location information based on a given place string.
    
    Parameters:
        place_string (str): The name of the place to search for.
        
    Returns:
        location_info (dict or None): A dictionary containing the latitude, longitude, and country of the location if found, or None if no location is found.
    """
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name": place_string,
        "count": 1,
        "language": "en",
        "format": "json"
    }
    response = requests.get(url, params=params)
    data = response.json()

    if "results" in data:
        result = data["results"][0]
        location_info = {
            "latitude": result["latitude"],
            "longitude": result["longitude"],
            "country": result["country"]
        }
        return location_info
    else:
        return None


def get_weather(period):
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    url = "https://api.open-meteo.com/v1/forecast"

    # Initialize params before conditional statements
    params = {
        "latitude": 52.5244,
        "longitude": 13.4105
    }

    if period == "current":
        params["current"] = ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "rain", "showers",
                             "snowfall", "weather_code", "surface_pressure", "wind_speed_10m", "wind_direction_10m",
                             "wind_gusts_10m"]
    elif period in ["today hourly", "tomorrow hourly", "day after tomorrow hourly"]:
        params["hourly"] = ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "rain", "showers",
                            "snowfall", "weather_code", "surface_pressure", "wind_speed_10m", "wind_direction_10m",
                            "wind_gusts_10m"]
        params["forecast_days"] = 3
    elif period in ["today", "tomorrow", "day after tomorrow"]:
        params["daily"] = ["weather_code", "temperature_2m_max", "temperature_2m_min", "apparent_temperature_max",
                           "apparent_temperature_min", "rain_sum", "showers_sum", "snowfall_sum", "wind_speed_10m_max",
                           "wind_gusts_10m_max", "wind_direction_10m_dominant"]
        params["forecast_days"] = 3
    elif period == "week":
        params["daily"] = ["weather_code", "temperature_2m_max", "temperature_2m_min", "apparent_temperature_max",
                           "apparent_temperature_min", "rain_sum", "showers_sum", "snowfall_sum", "wind_speed_10m_max",
                           "wind_gusts_10m_max", "wind_direction_10m_dominant"]
        params["forecast_days"] = 7

    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]
    return response
