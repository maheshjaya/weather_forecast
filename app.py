from flask import Flask, request, jsonify, send_from_directory
import requests
import time
import os

app = Flask(__name__)
API_KEY = os.getenv("API_KEY")  # Secure API key from Render settings

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/weather')
def get_weather():
    city = request.args.get('city')
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
    geo_data = requests.get(geo_url).json()
    if not geo_data:
        return jsonify({'error': 'City not found'}), 404

    lat = geo_data[0]['lat']
    lon = geo_data[0]['lon']
    
    now = int(time.time())
    temps = []
    for i in range(1, 6):  # last 5 days
        dt = now - i * 86400
        url = f"https://api.openweathermap.org/data/2.5/onecall/timemachine"
        params = {
            'lat': lat,
            'lon': lon,
            'dt': dt,
            'appid': API_KEY,
            'units': 'metric'
        }
        data = requests.get(url, params=params).json()
        temp = data['current']['temp']
        date = time.strftime('%Y-%m-%d', time.localtime(dt))
        temps.append({'date': date, 'temp': temp})

    return jsonify(temps)

if __name__ == '__main__':
    app.run()
