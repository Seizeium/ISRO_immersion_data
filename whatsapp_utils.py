import logging
from flask import current_app, jsonify
import json
import requests
#from app.services.openai_service import generate_response
import re


def log_http_response(response):
    logging.info(f"Status: {response.status_code}")
    logging.info(f"Content-type: {response.headers.get('content-type')}")
    logging.info(f"Body: {response.text}")

def get_text_message_input(recipient, text):
    return json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient,
            "type": "text",
            "text": {"preview_url": False, "body": text},
        }
    )

def send_whatsapp_image():
    url = "https://graph.facebook.com/v13.0/391717047356634/messages"
    headers = {
        "Authorization": "Bearer EAAMqtMoSZAi0BO2WBg26PMqxianlJAQMZBoTmKtxm3TUw233Wt4dvzjXwY4tiyRTx0BA2Yw28UxZAY7etXzieZAgTJA3JBSeD34zPZBwHZANnNpVn77vUUEmbe1qV6QBi35zSrBPHeZCr6MZAmJpDt8TCmW0iE1SbDLguiMZCJVRbDvJFqEXq680TipdlissKqnaJ2AUZBZCSX9p2cJzzjnfJi7gL3xxZBDVsOCyzC4ZD",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": "+919405720785",
        "type": "image",
        "image": {
            "link": "https://www.python.org/static/img/python-logo.png"
        }
    }

    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        print("Message sent successfully")
    else:
        print(f"Failed to send message. Status code: {response.status_code}, Response: {response.text}")

def request_user_location():
    url = "https://graph.facebook.com/v13.0/391717047356634/messages"
    headers = {
        "Authorization": "Bearer EAAMqtMoSZAi0BO2WBg26PMqxianlJAQMZBoTmKtxm3TUw233Wt4dvzjXwY4tiyRTx0BA2Yw28UxZAY7etXzieZAgTJA3JBSeD34zPZBwHZANnNpVn77vUUEmbe1qV6QBi35zSrBPHeZCr6MZAmJpDt8TCmW0iE1SbDLguiMZCJVRbDvJFqEXq680TipdlissKqnaJ2AUZBZCSX9p2cJzzjnfJi7gL3xxZBDVsOCyzC4ZD",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": "+919405720785",
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {
                "text": "Hey there! Would you like to share your location with us to get started?"
            },
            "action": {
                "buttons": [
                    {
                        "type": "reply",
                        "reply": {
                            "id": "yes_location",
                            "title": "Yes, share location"
                        }
                    },
                    {
                        "type": "reply",
                        "reply": {
                            "id": "no_location",
                            "title": "No, thanks"
                        }
                    }
                ]
            }
        }
    }


    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        print("Location request sent successfully")
    else:
        print(f"Failed to send location request. Status code: {response.status_code}, Response: {response.text}")


#def generate_response(response):
#    text = "Hey there!, How can I help you today ?"
#    return text


def send_message(data):
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {current_app.config['ACCESS_TOKEN']}",
    }

    url = f"https://graph.facebook.com/{current_app.config['VERSION']}/{current_app.config['PHONE_NUMBER_ID']}/messages"

    try:
        response = requests.post(
            url, data=data, headers=headers, timeout=10
        )  # 10 seconds timeout as an example
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
    except requests.Timeout:
        logging.error("Timeout occurred while sending message")
        return jsonify({"status": "error", "message": "Request timed out"}), 408
    except (
        requests.RequestException
    ) as e:  # This will catch any general request exception
        logging.error(f"Request failed due to: {e}")
        return jsonify({"status": "error", "message": "Failed to send message"}), 500
    else:
        # Process the response as normal
        log_http_response(response)
        return response
    

def process_text_for_whatsapp(text):
    # Remove brackets
    pattern = r"\【.*?\】"
    # Substitute the pattern with an empty string
    text = re.sub(pattern, "", text).strip()

    # Pattern to find double asterisks including the word(s) in between
    pattern = r"\*\*(.*?)\*\*"

    # Replacement pattern with single asterisks
    replacement = r"*\1*"

    # Substitute occurrences of the pattern with the replacement
    whatsapp_style_text = re.sub(pattern, replacement, text)

    return whatsapp_style_text


def process_whatsapp_message(body):
    wa_id = body["entry"][0]["changes"][0]["value"]["contacts"][0]["wa_id"]
    name = body["entry"][0]["changes"][0]["value"]["contacts"][0]["profile"]["name"]

    message = body["entry"][0]["changes"][0]["value"]["messages"][0]

    message_body = None

    if message["type"] == "text":
        message_body = message["text"]["body"]
        print(f"Received text message from {name} ({wa_id}): {message_body}")
    elif message["type"] == "location":
        location = message["location"]
        latitude = location["latitude"]
        longitude = location["longitude"]
        print(f"Received location from {name} ({wa_id}): Latitude: {latitude}, Longitude: {longitude}")

        weather_data = get_weather_data(latitude, longitude)
        if weather_data:
            formatted_weather  = format_weather_data(weather_data)
            data = get_text_message_input(current_app.config["RECIPIENT_WAID"], formatted_weather)
            send_message(data)
        # Example usage
        #latitude = 28.7041  # Replace with your latitude
        #longitude = 77.1025 # Replace with your longitude
    else:
        message_body = None
        print(f"Received unsupported message type from {name} ({wa_id})")

    # TODO: implement custom function here
    #response = generate_response(message_body)

    # OpenAI Integration
    #response = generate_response(message_body, wa_id, name)
    #response = process_text_for_whatsapp(response)

    data = get_text_message_input(current_app.config["RECIPIENT_WAID"], response)
    send_message(data)


def is_valid_whatsapp_message(body):
    """
    Check if the incoming webhook event has a valid WhatsApp message structure.
    """
    return (
        body.get("object")
        and body.get("entry")
        and body["entry"][0].get("changes")
        and body["entry"][0]["changes"][0].get("value")
        and body["entry"][0]["changes"][0]["value"].get("messages")
        and body["entry"][0]["changes"][0]["value"]["messages"][0]
    )
#send_whatsapp_image()
request_user_location()


import requests

def get_weather_data(latitude, longitude):
    # Open Meteo API endpoint
    url = "https://api.open-meteo.com/v1/forecast"
    
    # Parameters for the API call
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m,precipitation,weathercode",
        "current_weather": "true"
    }
    
    # Make the API request
    response = requests.get(url, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Error:", response.status_code)
        return None

def format_weather_data(weather_data):
    current_weather = weather_data.get('current_weather')
    
    if current_weather:
        temperature = current_weather.get('temperature')
        windspeed = current_weather.get('windspeed')
        winddirection = current_weather.get('winddirection')
        weathercode = current_weather.get('weathercode')

        weathercode_meaning = {
            0: "Clear sky ☀️",
            1: "Mainly clear 🌤",
            2: "Partly cloudy ⛅",
            3: "Overcast ☁️",
            45: "Fog 🌫",
            48: "Depositing rime fog 🌫❄️",
            51: "Light drizzle 🌦",
            53: "Moderate drizzle 🌧",
            55: "Dense drizzle 🌧🌧",
            56: "Freezing drizzle 🌧❄️",
            57: "Dense freezing drizzle 🌧❄️",
            61: "Slight rain shower 🌦",
            63: "Moderate rain shower 🌧",
            65: "Violent rain shower 🌧🌧",
            66: "Freezing rain 🌧❄️",
            67: "Heavy freezing rain 🌧❄️",
            71: "Slight snow fall 🌨",
            73: "Moderate snow fall 🌨🌨",
            75: "Heavy snow fall 🌨❄️",
            77: "Snow grains 🌨",
            80: "Slight rain showers 🌦",
            81: "Moderate rain showers 🌧",
            82: "Violent rain showers 🌧🌧",
            85: "Slight snow showers 🌨",
            86: "Heavy snow showers 🌨❄️",
            95: "Thunderstorm ⛈",
            96: "Thunderstorm with slight hail ⛈🌨",
            99: "Thunderstorm with heavy hail ⛈🌨"
        }

        weather_description = weathercode_meaning.get(weathercode, "Unknown weather code")

        formatted_data = (
            f"🌤️ *Current Weather Update* 🌤️\n\n"
            f"🌡️ *Temperature*: {temperature} °C\n"
            f"💨 *Wind Speed*: {windspeed} km/h\n"
            f"🧭 *Wind Direction*: {winddirection} °\n"
            f"🌥️ *Condition*: {weather_description}\n"
        )
        return formatted_data
    else:
        return "No current weather data available."



