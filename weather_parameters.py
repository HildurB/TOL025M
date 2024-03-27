def find_weather_type(doc):
  weather_types = ["weather", "temperature", "rain", "snow", "wind", "pressure", "humidity"]
  tokens = [token.text for token in doc]
  weather_types_found = []
  
  for token in tokens:
    if token.lower() in weather_types:
      weather_types_found.append(token)
      
  return weather_types_found

def find_location(doc):
  places = []
  for entity in doc.ents:
    if entity.label_ == 'GPE':
      places.append(entity.text)
  
  return places

def check_phrases(sentence, phrases):
    for phrase in phrases:
        if phrase in sentence.lower():
            return True
    return False

def find_forecast_period(user_input):
  current = ["today", "at the moment", "current", "currrently", "now", "right now"]
  day_after_tomorrow = ["day after tomorrow", "two days from now", "the day following tomorrow", "in two days"]
  this_week = ["this week", "next few days", "next couple of days"]
  hour  = ["hourly", "hour", "detailed", "detail"]
  
  if check_phrases(user_input, current):
    return "current"
  elif "today" in user_input:
    if check_phrases(user_input, hour):
      return "today hourly"
    else:
      return "today"
  elif "tomorrow" in user_input:
    if check_phrases(user_input, hour):
      return "tomorrow hourly"
    else:
      return "tomorrow"
  elif check_phrases(user_input, day_after_tomorrow):
    if check_phrases(user_input, hour):
      return "day after tomorrow hourly"
    else:
      return "day after tomorrow"
  elif check_phrases(user_input, this_week):
    return "week"
  else:
    return "current"
