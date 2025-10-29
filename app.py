import os
import requests
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify

# Load environment variables
load_dotenv()

app = Flask(__name__)

class WeatherApp:
    def __init__(self):
        self.api_key = os.getenv('OPENWEATHER_API_KEY')
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
    
    def get_weather(self, city_name):
        """Fetch weather data for a given city"""
        if not self.api_key:
            return {'error': 'API key not configured'}
        
        # Remove any quotes from the city name
        city_name = city_name.strip('"\'')
        
        params = {
            'q': city_name,
            'appid': self.api_key,
            'units': 'metric'
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            
            if response.status_code == 401:
                return {'error': 'Invalid API key. Please check your OpenWeatherMap API key.'}
            elif response.status_code == 404:
                return {'error': f'City "{city_name}" not found. Please check the spelling.'}
            elif response.status_code != 200:
                return {'error': f'API Error: {response.status_code} - {response.reason}'}
                
            data = response.json()
            
            # Format the response
            return {
                'city': data['name'],
                'country': data['sys']['country'],
                'temperature': round(data['main']['temp']),
                'feels_like': round(data['main']['feels_like']),
                'humidity': data['main']['humidity'],
                'description': data['weather'][0]['description'].title(),
                'wind_speed': data['wind']['speed'],
                'icon': data['weather'][0]['icon']
            }
            
        except requests.exceptions.ConnectionError:
            return {'error': 'Network error: Please check your internet connection.'}
        except Exception as e:
            return {'error': f'Error fetching weather data: {str(e)}'}

# Initialize weather app
weather_app = WeatherApp()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def get_weather():
    city = request.json.get('city', '').strip()
    if not city:
        return jsonify({'error': 'Please enter a city name'})
    
    weather_data = weather_app.get_weather(city)
    return jsonify(weather_data)

if __name__ == '__main__':
    app.run(debug=True)