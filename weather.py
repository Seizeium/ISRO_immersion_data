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

# Example usage
# latitude = 28.7041  # Replace with your latitude
# longitude = 77.1025 # Replace with your longitude

weather_data = get_weather_data(latitude, longitude)
if weather_data:
    formatted_weather = format_weather_data(weather_data)
    print(formatted_weather)
