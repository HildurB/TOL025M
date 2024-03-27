def get_current_weather(response_from_api, places, types, weather_codes):
    print("current")
    current = response_from_api.Current()
    current_temperature_2m = round(current.Variables(0).Value(), 1)
    current_relative_humidity_2m = round(current.Variables(1).Value(), 1)
    current_apparent_temperature = round(current.Variables(2).Value(), 1)
    current_rain = round(current.Variables(3).Value(), 1)
    current_showers = round(current.Variables(4).Value(), 1)
    current_snowfall = round(current.Variables(5).Value(), 1)
    current_weather_code = round(current.Variables(6).Value(), 1)
    current_surface_pressure = round(current.Variables(7).Value(), 1)
    current_wind_speed_10m = round(current.Variables(8).Value(), 1)
    current_wind_direction_10m = round(current.Variables(9).Value(), 1)
    current_wind_gusts_10m = round(current.Variables(10).Value(), 1)
    response = ""
    # specific information
    if 'wind' in types:
        response += "The current wind speed in {} is {} m/s with gusts at {} m/s from {} degrees. ".format(places[0], round(0.277778 * current_wind_speed_10m, 1), round(0.277778 * current_wind_gusts_10m,1), current_wind_direction_10m)
    if 'temperature' in types:
        response += "The current temperature in {} is {} degrees Celsius. Feels like {} degrees Celsius.".format(places[0],current_temperature_2m, current_apparent_temperature)
    if 'pressure' in types:
        response += "The current air pressure in {} is {} hPa. ".format(places[0],current_surface_pressure)
    if 'humidity' in types:
        response += "The current humidity in {} is {}%. ".format(places[0],current_relative_humidity_2m)
    if 'snow' in types:
        response += "The current snowfall in {} is {} cm. ".format(places[0],current_snowfall)
    if 'rain' in types:
        response += "The current rain in {} is {}mm with showers of {}mm. ".format(places[0],current_rain, current_showers)
    # generic query
    if 'weather' in types and response  == "":
        response="The current temperature in {} is {} degrees Celsius, which feels like {} degrees Celsius. It is {} and the wind speed is {}m/s".format(places[0], current_temperature_2m,current_apparent_temperature, weather_codes[current_weather_code], current_wind_speed_10m)
    return response