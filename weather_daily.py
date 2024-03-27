import pandas as pd


def format_wind_data(df):
    """
    A function to format wind data from a DataFrame and add it to a response string.
    
    Parameters:
    - df (pandas.DataFrame): DataFrame containing all the data
    - response (str): String representing an HTML response
    
    Returns:
    - response: Updated HTML response with formatted wind data added
    """
    response = ""
    for i in range(len(df)):
        formatted_time = pd.to_datetime(df["date"][i]).strftime("%d.%b")
        wind_speed = round(0.277778 * df["wind_speed_10m_max"][i], 1)
        wind_direction = df["wind_direction_10m_dominant"][i]
        wind_gusts = round(0.277778 * df["wind_gusts_10m_max"][i], 1)
        response += f"<p>{formatted_time}: maximum wind speed of {wind_speed:.1f} m/s with gusts at maximum {wind_gusts:.1f} m/s from dominant direction at {wind_direction} degrees.</p>"
    return response


def format_temperature_data(df):
    """
    A function to format temperature data from a DataFrame and add it to a response string.

    Args:
        df (pandas.DataFrame): The DataFrame containing all the data
        response (str): The string to which the formatted temperature data will be appended.

    Returns:
        str: The updated string containing the formatted temperature data.
    """
    response = ""
    for i in range(len(df)):
        formatted_time = pd.to_datetime(df["date"][i]).strftime("%d.%b")
        temperature_max = round(df["temperature_2m_max"][i], 1)
        temperature_min = round(df["temperature_2m_min"][i], 1)
        apparent_temperature_max = round(df["apparent_temperature_max"][i], 1)
        apparent_temperature_min = round(df["apparent_temperature_min"][i], 1)
        response += f"<p>{formatted_time}: temperature from {temperature_min:.1f} to {temperature_max:.1f}°C. Feels like from {apparent_temperature_min:.1f} to {apparent_temperature_max:.1f}°C.</p>"
    return response

# Function to format humidity data


def format_humidity_data(df):
    """
    A function to format humidity data from a DataFrame and add it to a response string.

    Parameters:
    - df (pandas.DataFrame): The DataFrame containing all the data
    - response (str): string representing the response to which the formatted data will be appended.

    Returns:
    - response: The updated string containing the formatted humidity data.
    """
    response = ""
    for i in range(len(df)):
        formatted_time = pd.to_datetime(df["date"][i]).strftime("%d.%b")
        humidity = round(df["relative_humidity_2m"][i], 1)
        response += f"<p>{formatted_time}: {humidity:.1f} %.</p>"
    return response

# Function to format snowfall data


def format_snowfall_data(df):
    """
    A function to format snowfall data from a DataFrame and add it to a response string.

    Parameters:
    - df (pandas.DataFrame): The DataFrame containing all the data
    - response (str): string representing the response to which the formatted data will be appended.

    Returns:
    - response: The updated string containing the formatted snowfall data.
    """
    response = ""
    for i in range(len(df)):
        formatted_time = pd.to_datetime(df["date"][i]).strftime("%d.%b")
        snowfall = round(df["snowfall_sum"][i], 1)
        response += f"<p>{formatted_time}: sum of {snowfall:.1f} cm.</p>"
    return response

# Function to format rain data


def format_rain_data(df):
    """
    A function to format rain data from a DataFrame and add it to a response string.

    Parameters:
    - df (pandas.DataFrame): The DataFrame containing all the data
    - response (str): string representing the response to which the formatted data will be appended.

    Returns:
    - response: The updated string containing the formatted rain data.
    """
    response = ""
    for i in range(len(df)):
        formatted_time = pd.to_datetime(df["date"][i]).strftime("%d.%b")
        rain = round(df["rain_sum"][i], 1)
        showers = round(df["showers_sum"][i], 1)
        response += f"<p>{formatted_time}: sum of rain {rain:.1f} mm with  showers of sum {showers:.1f} mm.</p>"
    return response

# Function to format generic weather data


def format_generic_weather_data(df):
    """
    A function to format generic weather data from a DataFrame and add it to a response string.

    Parameters:
    - df (pandas.DataFrame): The DataFrame containing all the data
    - response (str): string representing the response to which the formatted data will be appended.

    Returns:
    - response: The updated string containing the formatted generic weather data.
    """
    response = ""
    for i in range(len(df)):
        formatted_time = pd.to_datetime(df["date"][i]).strftime("%d.%b")
        temperature_min = round(df["temperature_2m_min"][i], 1)
        temperature_max = round(df["temperature_2m_max"][i], 1)
        apparent_temperature_min = round(df["apparent_temperature_min"][i], 1)
        apparent_temperature_max = round(df["apparent_temperature_max"][i], 1)
        weather_code = round(df["weather_code"][i], 1)
        wind_speed_max = round(0.277778 * df["wind_speed_10m_max"][i], 1)
        response += f"<p>{formatted_time}: temperature ranging from {temperature_min:.1f} to {temperature_max:.1f}°C which feels like {apparent_temperature_min:.1f} to {apparent_temperature_max:.1f}°C. It is {weather_code} and the maximum wind speed is at {wind_speed_max:.1f} m/s.</p>"
    return response


def process_daily_data(response_from_api):
    """
    Process daily data and return a pandas DataFrame.

    Parameters:
        response_from_api (object): The response object from the API.

    Returns:
        pandas.DataFrame: A DataFrame containing the processed daily data.
    """
    # Process daily data. The order of variables needs to be the same as requested.
    daily = response_from_api.Daily()
    daily_weather_code = daily.Variables(0).ValuesAsNumpy()
    daily_temperature_2m_max = daily.Variables(1).ValuesAsNumpy()
    daily_temperature_2m_min = daily.Variables(2).ValuesAsNumpy()
    daily_apparent_temperature_max = daily.Variables(3).ValuesAsNumpy()
    daily_apparent_temperature_min = daily.Variables(4).ValuesAsNumpy()
    daily_rain_sum = daily.Variables(5).ValuesAsNumpy()
    daily_showers_sum = daily.Variables(6).ValuesAsNumpy()
    daily_snowfall_sum = daily.Variables(7).ValuesAsNumpy()
    daily_wind_speed_10m_max = daily.Variables(8).ValuesAsNumpy()
    daily_wind_gusts_10m_max = daily.Variables(9).ValuesAsNumpy()
    daily_wind_direction_10m_dominant = daily.Variables(10).ValuesAsNumpy()

    daily_data = {"date": pd.date_range(
        start=pd.to_datetime(daily.Time(), unit="s", utc=True),
        end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=daily.Interval()),
        inclusive="left"
    )}
    daily_data["weather_code"] = daily_weather_code
    daily_data["temperature_2m_max"] = daily_temperature_2m_max
    daily_data["temperature_2m_min"] = daily_temperature_2m_min
    daily_data["apparent_temperature_max"] = daily_apparent_temperature_max
    daily_data["apparent_temperature_min"] = daily_apparent_temperature_min
    daily_data["rain_sum"] = daily_rain_sum
    daily_data["showers_sum"] = daily_showers_sum
    daily_data["snowfall_sum"] = daily_snowfall_sum
    daily_data["wind_speed_10m_max"] = daily_wind_speed_10m_max
    daily_data["wind_gusts_10m_max"] = daily_wind_gusts_10m_max
    daily_data["wind_direction_10m_dominant"] = daily_wind_direction_10m_dominant

    daily_dataframe = pd.DataFrame(data=daily_data)
    return daily_dataframe


def process_daily_data_today(response_from_api):
    """
    Precess daily data for the current day and return a pandas DataFrame.
    
    Parameters:
        response_from_api (object): The response object from the API.

    Returns:
        pandas.DataFrame: A DataFrame containing the processed daily data.
    """
    # Process daily data. The order of variables needs to be the same as requested.
    daily = response_from_api.Daily()
    daily_weather_code = daily.Variables(0).ValuesAsNumpy()[:-2]
    daily_temperature_2m_max = daily.Variables(1).ValuesAsNumpy()[:-2]
    daily_temperature_2m_min = daily.Variables(2).ValuesAsNumpy()[:-2]
    daily_apparent_temperature_max = daily.Variables(3).ValuesAsNumpy()[:-2]
    daily_apparent_temperature_min = daily.Variables(4).ValuesAsNumpy()[:-2]
    daily_rain_sum = daily.Variables(5).ValuesAsNumpy()[:-2]
    daily_showers_sum = daily.Variables(6).ValuesAsNumpy()[:-2]
    daily_snowfall_sum = daily.Variables(7).ValuesAsNumpy()[:-2]
    daily_wind_speed_10m_max = daily.Variables(8).ValuesAsNumpy()[:-2]
    daily_wind_gusts_10m_max = daily.Variables(9).ValuesAsNumpy()[:-2]
    daily_wind_direction_10m_dominant = daily.Variables(10).ValuesAsNumpy()[
        :-2]

    daily_data = {"date": pd.date_range(
        start=pd.to_datetime(daily.Time(), unit="s", utc=True),
        end=pd.to_datetime(daily.TimeEnd(), unit="s",
                           utc=True) - pd.Timedelta(days=2),
        freq=pd.Timedelta(seconds=daily.Interval()),
        inclusive="left"
    )}
    daily_data["weather_code"] = daily_weather_code
    daily_data["temperature_2m_max"] = daily_temperature_2m_max
    daily_data["temperature_2m_min"] = daily_temperature_2m_min
    daily_data["apparent_temperature_max"] = daily_apparent_temperature_max
    daily_data["apparent_temperature_min"] = daily_apparent_temperature_min
    daily_data["rain_sum"] = daily_rain_sum
    daily_data["showers_sum"] = daily_showers_sum
    daily_data["snowfall_sum"] = daily_snowfall_sum
    daily_data["wind_speed_10m_max"] = daily_wind_speed_10m_max
    daily_data["wind_gusts_10m_max"] = daily_wind_gusts_10m_max
    daily_data["wind_direction_10m_dominant"] = daily_wind_direction_10m_dominant

    daily_dataframe = pd.DataFrame(data=daily_data)
    return daily_dataframe


def process_daily_data_tomorrow(response_from_api):
    """
    Precess daily data for the tomorrow and return a pandas DataFrame.
    
    Parameters:
        response_from_api (object): The response object from the API.

    Returns:
        pandas.DataFrame: A DataFrame containing the processed daily data.
    """
    # Process daily data. The order of variables needs to be the same as requested.
    daily = response_from_api.Daily()
    daily_weather_code = daily.Variables(0).ValuesAsNumpy()[1:-1]
    daily_temperature_2m_max = daily.Variables(1).ValuesAsNumpy()[1:-1]
    daily_temperature_2m_min = daily.Variables(2).ValuesAsNumpy()[1:-1]
    daily_apparent_temperature_max = daily.Variables(3).ValuesAsNumpy()[1:-1]
    daily_apparent_temperature_min = daily.Variables(4).ValuesAsNumpy()[1:-1]
    daily_rain_sum = daily.Variables(5).ValuesAsNumpy()[1:-1]
    daily_showers_sum = daily.Variables(6).ValuesAsNumpy()[1:-1]
    daily_snowfall_sum = daily.Variables(7).ValuesAsNumpy()[1:-1]
    daily_wind_speed_10m_max = daily.Variables(8).ValuesAsNumpy()[1:-1]
    daily_wind_gusts_10m_max = daily.Variables(9).ValuesAsNumpy()[1:-1]
    daily_wind_direction_10m_dominant = daily.Variables(10).ValuesAsNumpy()[
        1:-1]

    daily_data = {"date": pd.date_range(
        start=pd.to_datetime(daily.Time(), unit="s",
                             utc=True) + pd.Timedelta(days=1),
        end=pd.to_datetime(daily.TimeEnd(), unit="s",
                           utc=True) - pd.Timedelta(days=1),
        freq=pd.Timedelta(seconds=daily.Interval()),
        inclusive="left"
    )}
    daily_data["weather_code"] = daily_weather_code
    daily_data["temperature_2m_max"] = daily_temperature_2m_max
    daily_data["temperature_2m_min"] = daily_temperature_2m_min
    daily_data["apparent_temperature_max"] = daily_apparent_temperature_max
    daily_data["apparent_temperature_min"] = daily_apparent_temperature_min
    daily_data["rain_sum"] = daily_rain_sum
    daily_data["showers_sum"] = daily_showers_sum
    daily_data["snowfall_sum"] = daily_snowfall_sum
    daily_data["wind_speed_10m_max"] = daily_wind_speed_10m_max
    daily_data["wind_gusts_10m_max"] = daily_wind_gusts_10m_max
    daily_data["wind_direction_10m_dominant"] = daily_wind_direction_10m_dominant

    daily_dataframe = pd.DataFrame(data=daily_data)
    return daily_dataframe


def process_daily_data_day_after_tomorrow(response_from_api):
    """
    Precess daily data for the day after tomorrow and return a pandas DataFrame.
    
    Parameters:
        response_from_api (object): The response object from the API.

    Returns:
        pandas.DataFrame: A DataFrame containing the processed daily data.
    """
    daily = response_from_api.Daily()
    daily_weather_code = daily.Variables(0).ValuesAsNumpy()[2:]
    daily_temperature_2m_max = daily.Variables(1).ValuesAsNumpy()[2:]
    daily_temperature_2m_min = daily.Variables(2).ValuesAsNumpy()[2:]
    daily_apparent_temperature_max = daily.Variables(3).ValuesAsNumpy()[2:]
    daily_apparent_temperature_min = daily.Variables(4).ValuesAsNumpy()[2:]
    daily_rain_sum = daily.Variables(5).ValuesAsNumpy()[2:]
    daily_showers_sum = daily.Variables(6).ValuesAsNumpy()[2:]
    daily_snowfall_sum = daily.Variables(7).ValuesAsNumpy()[2:]
    daily_wind_speed_10m_max = daily.Variables(8).ValuesAsNumpy()[2:]
    daily_wind_gusts_10m_max = daily.Variables(9).ValuesAsNumpy()[2:]
    daily_wind_direction_10m_dominant = daily.Variables(10).ValuesAsNumpy()[2:]

    daily_data = {"date": pd.date_range(
        start=pd.to_datetime(daily.Time(), unit="s",
                             utc=True) + pd.Timedelta(days=2),
        end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=daily.Interval()),
        inclusive="left"
    )}
    daily_data["weather_code"] = daily_weather_code
    daily_data["temperature_2m_max"] = daily_temperature_2m_max
    daily_data["temperature_2m_min"] = daily_temperature_2m_min
    daily_data["apparent_temperature_max"] = daily_apparent_temperature_max
    daily_data["apparent_temperature_min"] = daily_apparent_temperature_min
    daily_data["rain_sum"] = daily_rain_sum
    daily_data["showers_sum"] = daily_showers_sum
    daily_data["snowfall_sum"] = daily_snowfall_sum
    daily_data["wind_speed_10m_max"] = daily_wind_speed_10m_max
    daily_data["wind_gusts_10m_max"] = daily_wind_gusts_10m_max
    daily_data["wind_direction_10m_dominant"] = daily_wind_direction_10m_dominant

    daily_dataframe = pd.DataFrame(data=daily_data)
    return daily_dataframe


def get_daily_data(types, response_from_api):
    """
    Generate a formatted response with weather data based on the types specified.

    Parameters:
        types (list): a list of strings specifying the types of weather data to include in the response
        response_from_api (dict): the response received from the API containing the weather data

    Returns:
        response (str): a formatted response containing the requested weather data
    """
    daily_dataframe = process_daily_data(response_from_api)
    response = "For weather for the next days is as follows:"
    if 'wind' in types:
        response += format_wind_data(daily_dataframe)
    if 'temperature' in types:
        response += format_temperature_data(daily_dataframe)
    if 'pressure' in types:
        response += "sorry I am not sure on the daily pressure yet"
    if 'humidity' in types:
        response += "sorry I am not sure on the humidity on the daily yet"
    if 'snow' in types:
        response += format_snowfall_data(daily_dataframe)
    if 'rain' in types:
        response += format_rain_data(daily_dataframe)
    if 'weather' in types:
        response += format_generic_weather_data(daily_dataframe)
    return response


def get_daily_data_today(types, response_from_api):
    """
    Generate a formatted response with weather data for today based on the types specified.

    Parameters:
        types (list): a list of strings specifying the types of weather data to include in the response
        response_from_api (dict): the response received from the API containing the weather data

    Returns:
        response (str): a formatted response containing the requested weather data
    """
    daily_dataframe = process_daily_data_today(response_from_api)
    response = ""
    if 'wind' in types:
        response += format_wind_data(daily_dataframe)
    if 'temperature' in types:
        response += format_temperature_data(daily_dataframe)
    if 'pressure' in types:
        response += "sorry I am not sure on the daily pressure yet"
    if 'humidity' in types:
        response += "sorry I am not sure on the humidity on the daily yet"
    if 'snow' in types:
        response += format_snowfall_data(daily_dataframe)
    if 'rain' in types:
        response += format_rain_data(daily_dataframe)
    if 'weather' in types:
        response += format_generic_weather_data(daily_dataframe)
    return response


def get_daily_data_tomorrow(types, response_from_api):
    """
    Generate a formatted response with weather data for tomorrow based on the types specified.

    Parameters:
        types (list): a list of strings specifying the types of weather data to include in the response
        response_from_api (dict): the response received from the API containing the weather data

    Returns:
        response (str): a formatted response containing the requested weather data
    """
    daily_dataframe = process_daily_data_tomorrow(response_from_api)
    response = ""
    if 'wind' in types:
        response += format_wind_data(daily_dataframe)
    if 'temperature' in types:
        response += format_temperature_data(daily_dataframe)
    if 'pressure' in types:
        response += "sorry I am not sure on the daily pressure yet"
    if 'humidity' in types:
        response += "sorry I am not sure on the humidity on the daily yet"
    if 'snow' in types:
        response += format_snowfall_data(daily_dataframe)
    if 'rain' in types:
        response += format_rain_data(daily_dataframe)
    if 'weather' in types:
        response += format_generic_weather_data(daily_dataframe)
    return response


def get_daily_data_day_after_tomorrow(types, response_from_api):
    """
    Generate a formatted response with weather data for the day after tomorrow based on the types specified.

    Parameters:
        types (list): a list of strings specifying the types of weather data to include in the response
        response_from_api (dict): the response received from the API containing the weather data

    Returns:
        response (str): a formatted response containing the requested weather data
    """
    daily_dataframe = process_daily_data_day_after_tomorrow(response_from_api)
    response = ""
    if 'wind' in types:
        response += format_wind_data(daily_dataframe)
    if 'temperature' in types:
        response += format_temperature_data(daily_dataframe)
    if 'pressure' in types:
        response += "sorry I am not sure on the daily pressure yet"
    if 'humidity' in types:
        response += "sorry I am not sure on the humidity on the daily yet"
    if 'snow' in types:
        response += format_snowfall_data(daily_dataframe)
    if 'rain' in types:
        response += format_rain_data(daily_dataframe)
    if 'weather' in types:
        response += format_generic_weather_data(daily_dataframe)
    return response
