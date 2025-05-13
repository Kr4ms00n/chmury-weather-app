import os
import datetime
import socket
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

AUTHOR_NAME = "Jakub Kramek"
PORT = int(os.environ.get("PORT", 5000))

COUNTRIES = {
    "poland": ["Warsaw", "Krakow", "Gdansk", "Wroclaw", "Poznan"],
    "germany": ["Berlin", "Munich", "Hamburg", "Frankfurt", "Cologne"],
    "france": ["Paris", "Marseille", "Lyon", "Toulouse", "Nice"],
    "uk": ["London", "Manchester", "Birmingham", "Glasgow", "Liverpool"],
    "usa": ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"]
}

WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY", "")

def log_startup_info():
    hostname = socket.gethostname()
    startup_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Application started at: {startup_time}")
    print(f"Author: {AUTHOR_NAME}")
    print(f"Listening on port: {PORT}")
    print(f"Hostname: {hostname}")

@app.route('/')
def index():
    return render_template('index.html', countries=COUNTRIES)

@app.route('/api/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    country = request.args.get('country')

    if not city or not country:
        return jsonify({"error": "Missing city or country"}), 400

    if country not in COUNTRIES or city not in COUNTRIES[country]:
        return jsonify({"error": "Invalid city or country"}), 400

    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        if response.status_code != 200:
            return jsonify({"error": f"Weather API error: {data.get('message', 'Unknown error')}"}), 500

        weather = {
            "city": city,
            "country": country,
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "description": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "icon": data["weather"][0]["icon"]
        }

        return jsonify(weather)

    except Exception as e:
        app.logger.error(f"Error fetching weather data: {str(e)}")
        return jsonify({"error": "Failed to fetch weather data"}), 500

if __name__ == '__main__':
    log_startup_info()
    app.run(host='0.0.0.0', port=PORT)
