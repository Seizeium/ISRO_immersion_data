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
                "text": "Would you like to share your location with us?"
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




def generate_response(response):
    text = "Length of your message: " + str(len(response))
    return text
    


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
    message_body = message["text"]["body"]


    # TODO: implement custom function here
    response = generate_response(message_body)

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
send_whatsapp_image()
request_user_location()
