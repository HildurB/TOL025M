from flask import Flask, render_template, request, jsonify, session
import spacy #python -m spacy download en_core_web_sm
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer;
import pandas as pd
from retry_requests import retry

import weather_current
import weather
import weather_parameters
import weather_hourly
import weather_daily

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to a random secret key for session management

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

rain_codes = [51, 53, 55, 61, 63, 65, 80, 81, 82]
snow_codes = [71, 73, 75, 85, 86]

nlp = spacy.load("en_core_web_sm")
chatbot = ChatBot("WeatherWizard")

trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train(
      "./greetings.yml",
      "chatterbot.corpus.english.greetings"
)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send-message', methods=['POST'])
def send_message():
    data = request.get_json()
    user_message = data['message']
    response = get_response(user_message)
    return  jsonify({'message': str(response)}) 

def give_response(forecast_period, types, places):
  location_info = weather.get_location_info(places[0])

  
  if location_info:
    response_from_api = weather.get_weather(forecast_period)
    
  response = ""
  if forecast_period == 'current': 
    response = weather_current.get_current_weather(response_from_api, places, types, weather_codes)
  elif forecast_period == "today":
    response = weather_daily.get_daily_data_today(types, response_from_api)
  elif forecast_period == "tomorrow":
    response = weather_daily.get_daily_data_tomorrow(types, response_from_api)
  elif forecast_period == "day after tomorrow":
    response = weather_daily.get_daily_data_day_after_tomorrow(types, response_from_api)
  elif forecast_period == "today hourly":
    response = weather_hourly.get_hourly_data_today(types, response_from_api)
  elif forecast_period == "tomorrow hourly":
    response = weather_hourly.get_hourly_data_tomorrow(types, response_from_api)
  elif forecast_period == "day after tomorrow hourly":
    response = weather_hourly.get_hourly_data_day_after_tomorrow(types, response_from_api)
  elif forecast_period == "week":
    response = weather_daily.get_daily_data(types, response_from_api)

  return response


def get_response(user_input):

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

"""
    
def generate_ai_response(user_input):
        user_input = input("You: ")
        
        if user_input.lower() in ["quit", "exit", "goodbye", "bye", "byebye"]:
          return "Goodbye!"
        
        # Process the text using SpaCy
        doc = nlp(user_input)
        # tokenize the text
        types =  weather_parameters.find_weather_type(doc)
        places = weather_parameters.find_location(doc)
        forecast_period = weather_parameters.find_forecast_period(user_input)
        
        if types:
          if places:
            response = give_response(forecast_period, types, places)
          else:
            response = "In what location do you want to know the weather?"
            print("Chatbot:", response)
            user_input2 = input("You: ")
            doc2 = nlp(user_input2)
            places = weather_parameters.find_location(doc2)
            if places:
              response = give_response(forecast_period, types, places)
            else:
              response = "I couldn't find information for the specified location."
        else:
          response = chatbot.get_response(user_input)
          #response = "Sorry, I am not sure what you are asking about. You can try asking about: wind, temperature, pressure, humidity, snow, rain or the general weather at some place."
        print("Chatbot:", response)
"""


if __name__ == '__main__':
    app.run(debug=True)

    
