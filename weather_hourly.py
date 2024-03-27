import pandas as pd

def format_wind_data(df): 
    response = ""
    for i in range(len(df)):
        formatted_time = pd.to_datetime(df["date"][i]).strftime("%H:%M")
        wind_speed = round(0.277778 * df["wind_speed_10m"][i], 1)  
        wind_direction = df["wind_direction_10m"][i]
        wind_gusts = round(0.277778 * df["wind_gusts_10m"][i], 1)  
        response += f"<p>{formatted_time}: wind speed of {wind_speed:.1f} m/s with gusts at {wind_gusts:.1f} m/s from {wind_direction} degrees.</p>"
    return response

# Function to format temperature data
def format_temperature_data(df): 
    response = ""
    for i in range(len(df)):
        formatted_time = pd.to_datetime(df["date"][i]).strftime("%H:%M")
        temperature = round(df["temperature_2m"][i], 1)  
        apparent_temperature = round(df["apparent_temperature"][i], 1)  
        response += f"<p>{formatted_time}: {temperature:.1f}°C. Feels like {apparent_temperature:.1f}°C.</p>"
    return response

# Function to format pressure data
def format_pressure_data(df): 
    response = ""
    for i in range(len(df)):
        formatted_time = pd.to_datetime(df["date"][i]).strftime("%H:%M")
        pressure = round(df["surface_pressure"][i], 1)  
        response += f"<p>{formatted_time}: {pressure:.1f} hPa.</p>"
    return response

# Function to format humidity data
def format_humidity_data(df): 
    response = ""
    for i in range(len(df)):
        formatted_time = pd.to_datetime(df["date"][i]).strftime("%H:%M")
        humidity = round(df["relative_humidity_2m"][i], 1)  
        response += f"<p>{formatted_time}: {humidity:.1f} %.</p>"
    return response

# Function to format snowfall data
def format_snowfall_data(df): 
    response = ""
    for i in range(len(df)):
        formatted_time = pd.to_datetime(df["date"][i]).strftime("%H:%M")
        snowfall = round(df["snowfall"][i], 1)  
        response += f"<p>{formatted_time}: {snowfall:.1f} cm.</p>"
    return response

# Function to format rain data
def format_rain_data(df): 
    response = ""
    for i in range(len(df)):
        formatted_time = pd.to_datetime(df["date"][i]).strftime("%H:%M")
        rain = round(df["rain"][i], 1)  
        showers = round(df["showers"][i], 1)  
        response += f"<p>{formatted_time}: rain {rain:.1f} mm with showers of {showers:.1f} mm.</p>"
    return response

# Function to format generic weather data
def format_generic_weather_data(df): 
    response = ""
    for i in range(len(df)):
        formatted_time = pd.to_datetime(df["date"][i]).strftime("%H:%M")
        temperature = round(df["temperature_2m"][i], 1)  
        apparent_temperature = round(df["apparent_temperature"][i], 1)  
        weather_code = round(df["weather_code"][i], 1)  
        wind_speed = round(0.277778 * df["wind_speed_10m"][i], 1)  
        response += f"<p>{formatted_time}: temperature of {temperature:.1f}°C which feels like {apparent_temperature:.1f}°C. It is {weather_code} and the wind speed is {wind_speed:.1f} m/s.</p>"
    return response


def process_hourly_data_today(response):
  # Process hourly data. The order of variables needs to be the same as requested.
  hourly = response.Hourly()
  hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()[:-48]
  hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()[:-48]
  hourly_apparent_temperature = hourly.Variables(2).ValuesAsNumpy()[:-48]
  hourly_rain = hourly.Variables(3).ValuesAsNumpy()[:-48]
  hourly_showers = hourly.Variables(4).ValuesAsNumpy()[:-48]
  hourly_snowfall = hourly.Variables(5).ValuesAsNumpy()[:-48]
  hourly_weather_code = hourly.Variables(6).ValuesAsNumpy()[:-48]
  hourly_surface_pressure = hourly.Variables(7).ValuesAsNumpy()[:-48]
  hourly_wind_speed_10m = hourly.Variables(8).ValuesAsNumpy()[:-48]
  hourly_wind_direction_10m = hourly.Variables(9).ValuesAsNumpy()[:-48]
  hourly_wind_gusts_10m = hourly.Variables(10).ValuesAsNumpy()[:-48]

  hourly_data = {"date": pd.date_range(
    start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
    end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True) - pd.Timedelta(days=2),
    freq = pd.Timedelta(seconds = hourly.Interval()),
    inclusive = "left"
  )}
  hourly_data["temperature_2m"] = hourly_temperature_2m
  hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
  hourly_data["apparent_temperature"] = hourly_apparent_temperature
  hourly_data["rain"] = hourly_rain
  hourly_data["showers"] = hourly_showers
  hourly_data["snowfall"] = hourly_snowfall
  hourly_data["weather_code"] = hourly_weather_code
  hourly_data["surface_pressure"] = hourly_surface_pressure
  hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
  hourly_data["wind_direction_10m"] = hourly_wind_direction_10m
  hourly_data["wind_gusts_10m"] = hourly_wind_gusts_10m

  hourly_dataframe = pd.DataFrame(data = hourly_data)
  return hourly_dataframe


from datetime import datetime, timedelta

def process_hourly_data_tomorrow(response):
    # Process hourly data for tomorrow.
    hourly = response.Hourly()

    # Extract hourly data
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()[24:-24]  # Exclude the first 24 values
    hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()[24:-24]
    hourly_apparent_temperature = hourly.Variables(2).ValuesAsNumpy()[24:-24]
    hourly_rain = hourly.Variables(3).ValuesAsNumpy()[24:-24]
    hourly_showers = hourly.Variables(4).ValuesAsNumpy()[24:-24]
    hourly_snowfall = hourly.Variables(5).ValuesAsNumpy()[24:-24]
    hourly_weather_code = hourly.Variables(6).ValuesAsNumpy()[24:-24]
    hourly_surface_pressure = hourly.Variables(7).ValuesAsNumpy()[24:-24]
    hourly_wind_speed_10m = hourly.Variables(8).ValuesAsNumpy()[24:-24]
    hourly_wind_direction_10m = hourly.Variables(9).ValuesAsNumpy()[24:-24]
    hourly_wind_gusts_10m = hourly.Variables(10).ValuesAsNumpy()[24:-24]

    hourly_data = {"date": pd.date_range(
      start = pd.to_datetime(hourly.Time(), unit = "s", utc = True)+ pd.Timedelta(days=1),
      end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True) - pd.Timedelta(days=1),
      freq = pd.Timedelta(seconds = hourly.Interval()),
      inclusive = "left"
    )}
    
    hourly_data["temperature_2m"] = hourly_temperature_2m
    hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
    hourly_data["apparent_temperature"] = hourly_apparent_temperature
    hourly_data["rain"] = hourly_rain
    hourly_data["showers"] = hourly_showers
    hourly_data["snowfall"] = hourly_snowfall
    hourly_data["weather_code"] = hourly_weather_code
    hourly_data["surface_pressure"] = hourly_surface_pressure
    hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
    hourly_data["wind_direction_10m"] = hourly_wind_direction_10m
    hourly_data["wind_gusts_10m"] = hourly_wind_gusts_10m

    return pd.DataFrame(data=hourly_data)

def process_hourly_data_day_after_tomorrow(response):
    # Process hourly data for the day after tomorrow.
    hourly = response.Hourly()
    
    # Extract hourly data arrays starting from index 48 (after the first 48 hours).
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()[48:]
    hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()[48:]
    hourly_apparent_temperature = hourly.Variables(2).ValuesAsNumpy()[48:]
    hourly_rain = hourly.Variables(3).ValuesAsNumpy()[48:]
    hourly_showers = hourly.Variables(4).ValuesAsNumpy()[48:]
    hourly_snowfall = hourly.Variables(5).ValuesAsNumpy()[48:]
    hourly_weather_code = hourly.Variables(6).ValuesAsNumpy()[48:]
    hourly_surface_pressure = hourly.Variables(7).ValuesAsNumpy()[48:]
    hourly_wind_speed_10m = hourly.Variables(8).ValuesAsNumpy()[48:]
    hourly_wind_direction_10m = hourly.Variables(9).ValuesAsNumpy()[48:]
    hourly_wind_gusts_10m = hourly.Variables(10).ValuesAsNumpy()[48:]
    
    hourly_data = {"date": pd.date_range(
      start = pd.to_datetime(hourly.Time(), unit = "s", utc = True)+ pd.Timedelta(days=2),
      end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
      freq = pd.Timedelta(seconds = hourly.Interval()),
      inclusive = "left"
    )}
    
    # Assign data arrays to the corresponding keys in hourly_data
    hourly_data["temperature_2m"] = hourly_temperature_2m
    hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
    hourly_data["apparent_temperature"] = hourly_apparent_temperature
    hourly_data["rain"] = hourly_rain
    hourly_data["showers"] = hourly_showers
    hourly_data["snowfall"] = hourly_snowfall
    hourly_data["weather_code"] = hourly_weather_code
    hourly_data["surface_pressure"] = hourly_surface_pressure
    hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
    hourly_data["wind_direction_10m"] = hourly_wind_direction_10m
    hourly_data["wind_gusts_10m"] = hourly_wind_gusts_10m

    # Create DataFrame from hourly_data
    hourly_dataframe = pd.DataFrame(data=hourly_data)
    return hourly_dataframe


def get_hourly_data_today(types, response_from_api):
  hourly_dataframe = process_hourly_data_today(response_from_api)
  response = "For today the weather is as follows:</p>"
  if 'wind' in types:
      response += format_wind_data(hourly_dataframe)
  if 'temperature' in types:
      response += format_temperature_data(hourly_dataframe)
  if 'pressure' in types:
      response += format_pressure_data(hourly_dataframe)
  if 'humidity' in types:
      response += format_humidity_data(hourly_dataframe)
  if 'snow' in types:
      response += format_snowfall_data(hourly_dataframe)
  if 'rain' in types:
      response += format_rain_data(hourly_dataframe)
  if 'weather' in types:
      response += format_generic_weather_data(hourly_dataframe)
  return response


def get_hourly_data_tomorrow(types, response_from_api):
  hourly_dataframe = process_hourly_data_tomorrow(response_from_api)
  response = "For tomorrow the weather is as follows:"
  if 'wind' in types:
      response += format_wind_data(hourly_dataframe)
  if 'temperature' in types:
      response += format_temperature_data(hourly_dataframe)
  if 'pressure' in types:
      response += format_pressure_data(hourly_dataframe)
  if 'humidity' in types:
      response += format_humidity_data(hourly_dataframe)
  if 'snow' in types:
      response += format_snowfall_data(hourly_dataframe)
  if 'rain' in types:
      response += format_rain_data(hourly_dataframe)
  if 'weather' in types:
      response += format_generic_weather_data(hourly_dataframe)
  return response


def get_hourly_data_day_after_tomorrow(types, response_from_api):
  hourly_dataframe = process_hourly_data_day_after_tomorrow(response_from_api)
  response = "For the day after tomorrow the weather is as follows:</p>"
  if 'wind' in types:
      response += format_wind_data(hourly_dataframe)
  if 'temperature' in types:
      response += format_temperature_data(hourly_dataframe)
  if 'pressure' in types:
      response += format_pressure_data(hourly_dataframe)
  if 'humidity' in types:
      response += format_humidity_data(hourly_dataframe)
  if 'snow' in types:
      response += format_snowfall_data(hourly_dataframe)
  if 'rain' in types:
      response += format_rain_data(hourly_dataframe)
  if 'weather' in types:
      response += format_generic_weather_data(hourly_dataframe)
  return response