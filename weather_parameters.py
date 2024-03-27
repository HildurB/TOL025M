def find_weather_type(doc):
    """
    Finds the weather types in a given document.

    Parameters:
        doc (spaCy document): The document to search for weather types.

    Returns:
        List[str]: A list of weather types found in the document.
    """
    weather_types = ["weather", "temperature", "rain",
                     "snow", "wind", "pressure", "humidity"]
    tokens = [token.text for token in doc]
    weather_types_found = []

    for token in tokens:
        if token.lower() in weather_types:
            weather_types_found.append(token)

    return weather_types_found


def find_location(doc):
    """
    Find and extract locations from the given document.

    Parameters:
        doc (spacy.Doc): The input document containing entities.

    Returns:
        list: A list of location entities extracted from the document.
    """
    places = []
    for entity in doc.ents:
        if entity.label_ == 'GPE':
            places.append(entity.text)

    return places


def check_phrases(sentence, phrases):
    """
    Check if any phrase from the list of phrases is present in the given sentence.

    Parameters:
        sentence (str): The sentence to search for phrases.
        phrases (list): A list of phrases to check against the sentence.

    Returns:
        bool: True if any phrase is found in the sentence, False otherwise.
    """
    for phrase in phrases:
        if phrase in sentence.lower():
            return True
    return False


def find_forecast_period(user_input):
    """
    Function to determine the forecast period based on user input phrases.

    Parameters:
        user_input: a string representing the user's input

    Returns:
        A string indicating the forecast period
    """
    current = ["today", "at the moment", "current",
               "currrently", "now", "right now"]
    day_after_tomorrow = ["day after tomorrow", "two days from now",
                          "the day following tomorrow", "in two days"]
    this_week = ["this week", "next few days", "next couple of days"]
    hour = ["hourly", "hour", "detailed", "detail"]

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
