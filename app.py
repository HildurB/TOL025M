from flask import Flask, render_template, request, jsonify, session
import spacy  # python -m spacy download en_core_web_sm
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import pandas as pd
from retry_requests import retry

import weather_current
import weather
import weather_parameters
import weather_hourly
import weather_daily

app = Flask(__name__)
# Change this to a random secret key for session management
app.secret_key = 'your_secret_key_here'

weather_codes = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Drizzle: Light intensity",
    53: "Drizzle: Moderate intensity",
    55: "Drizzle: Dense intensity",
    56: "Freezing Drizzle: Light intensity",
    57: "Freezing Drizzle: Dense intensity",
    61: "Rain: Slight intensity",
    63: "Rain: Moderate intensity",
    65: "Rain: Heavy intensity",
    66: "Freezing Rain: Light intensity",
    67: "Freezing Rain: Heavy intensity",
    71: "Snow fall: Slight intensity",
    73: "Snow fall: Moderate intensity",
    75: "Snow fall: Heavy intensity",
    77: "Snow grains",
    80: "Rain showers: Slight intensity",
    81: "Rain showers: Moderate intensity",
    82: "Rain showers: Violent intensity",
    85: "Snow showers: Slight intensity",
    86: "Snow showers: Heavy intensity",
    95: "Thunderstorm: Slight intensity",
    96: "Thunderstorm with hail: Slight intensity",
    99: "Thunderstorm with hail: Heavy intensity"
}

nlp = spacy.load("en_core_web_sm")
chatbot = ChatBot("WeatherWizard")

trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train(
    "./greetings.yml",
    "chatterbot.corpus.english.greetings"
)


@app.route('/')
def index():
    """
    A route decorator for the index page that renders the index.html template.
    """
    return render_template('index.html')


@app.route('/send-message', methods=['POST'])
def send_message():
    """
    A function to send a message and get a response.
    """
    data = request.get_json()
    user_message = data['message']
    response = get_response(user_message)
    return jsonify({'message': str(response)})


def give_response(forecast_period, types, places):
    """
    Generate a response based on the forecast period, types, and locations provided.

    Args:
        forecast_period (str): The time period for which the weather forecast is requested.
        types (list): The types of weather data to retrieve.
        places (list): The locations for which weather information is needed.

    Returns:
        str: The response containing weather data based on the forecast period.
    """
    location_info = weather.get_location_info(places[0])

    if location_info:
        response_from_api = weather.get_weather(forecast_period)

    response = ""
    if forecast_period == 'current':
        response = weather_current.get_current_weather(
            response_from_api, places, types, weather_codes)
    elif forecast_period == "today":
        response = weather_daily.get_daily_data_today(types, response_from_api)
    elif forecast_period == "tomorrow":
        response = weather_daily.get_daily_data_tomorrow(
            types, response_from_api)
    elif forecast_period == "day after tomorrow":
        response = weather_daily.get_daily_data_day_after_tomorrow(
            types, response_from_api)
    elif forecast_period == "today hourly":
        response = weather_hourly.get_hourly_data_today(
            types, response_from_api)
    elif forecast_period == "tomorrow hourly":
        response = weather_hourly.get_hourly_data_tomorrow(
            types, response_from_api)
    elif forecast_period == "day after tomorrow hourly":
        response = weather_hourly.get_hourly_data_day_after_tomorrow(
            types, response_from_api)
    elif forecast_period == "week":
        response = weather_daily.get_daily_data(types, response_from_api)

    return response


def get_response(user_input):
    """
    This function takes in a user input and processes it to generate a response. It uses SpaCy to process the text and extract relevant information. 
    If the user's previous message was "In what location do you want to know the weather?", it extracts the location, weather type, and forecast period from the user input. 
    Otherwise, it extracts the weather type, location, and forecast period from the user input. If the weather type is found, it calls the 'give_response' function with the extracted parameters. 
    If the weather type is not found, it uses a chatbot to generate a response. The function returns the generated response.
    """

    # Process the text using SpaCy
    doc = nlp(user_input)

    if 'previous_message' in session and session['previous_message'] == "In what location do you want to know the weather?":
        places = weather_parameters.find_location(doc)
        types = session.get('types')
        forecast_period = session.get('forecast_period')
    else:
        types = weather_parameters.find_weather_type(doc)
        places = weather_parameters.find_location(doc)
        forecast_period = weather_parameters.find_forecast_period(user_input)
        session['types'] = types
        session['forecast_period'] = forecast_period

    if types:
        if places:
            response = give_response(forecast_period, types, places)
        else:
            response = "In what location do you want to know the weather?"
    else:
        response = chatbot.get_response(user_input).text

    session['previous_message'] = response
    return response

if __name__ == '__main__':
    app.run(debug=True)
