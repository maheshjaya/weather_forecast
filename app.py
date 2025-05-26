from flask import Flask, request, jsonify, send_from_directory
import requests
import time
import os

app = Flask(__name__)
API_KEY = os.getenv("API_KEY")  # Get API key from Render environment variable

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/weather')
def get_weather():
    city = request.args.get('city')

    # Get latitude and longitude of the city
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
    geo_data = requests.get(geo_url).json()
    if not geo_data:
        return jsonify({'error': 'City not found'}), 404

    lat = geo_data[0]['lat']
    lon = geo_data[0]['lon']

    now = int(time.time())
    temps = []

    # Get data for last 5 days
    for i in range(1, 6):
        dt = now - i * 86400  # subtract i days in seconds
        url = "https://api.openweathermap.org/data/2.5/onecall/timemachine"
        params = {
            'lat': lat,
            'lon': lon,
            'dt': dt,
            'appid': API_KEY,
            'units': 'metric'
        }
        data = requests.get(url, params=params).json()

        if 'current' not in data:
            continue  # skip if API fails

        temp = data['current']['temp']
        date = time.strftime('%Y-%m-%d', time.localtime(dt))
        temps.append({'date': date, 'temp': temp})

    return jsonify(temps)

# Correct deployment binding for Render
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
