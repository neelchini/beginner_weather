import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class WeatherApp:
    def __init__(self):
        self.api_key = os.getenv('OPENWEATHER_API_KEY')
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
        
        if not self.api_key:
            raise ValueError("❌ Please set OPENWEATHER_API_KEY in your .env file")
        
        # Test the API key immediately
        self.test_api_key()
    
    def test_api_key(self):
        """Test if the API key is valid"""
        test_params = {
            'q': 'London',
            'appid': self.api_key,
            'units': 'metric'
        }
        
        try:
            response = requests.get(self.base_url, params=test_params)
            if response.status_code == 401:
                print("❌ API Key Error: Invalid API key. Please check your OpenWeatherMap API key.")
                print("💡 New API keys can take 10-20 minutes to activate.")
            elif response.status_code != 200:
                print(f"⚠️  API returned status: {response.status_code}")
        except Exception as e:
            print(f"🌐 Network error: {e}")
    
    def get_weather(self, city_name):
        """Fetch weather data for a given city"""
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
                print("❌ Invalid API key. Please check your OpenWeatherMap API key.")
                return None
            elif response.status_code == 404:
                print(f"❌ City '{city_name}' not found. Please check the spelling.")
                return None
            elif response.status_code != 200:
                print(f"❌ API Error: {response.status_code} - {response.reason}")
                return None
                
            return response.json()
            
        except requests.exceptions.ConnectionError:
            print("❌ Network error: Please check your internet connection.")
            return None
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching weather data: {e}")
            return None
    
    def display_weather(self, weather_data):
        """Display weather information in a readable format"""
        if not weather_data:
            return
        
        # Extract relevant information
        city = weather_data['name']
        country = weather_data['sys']['country']
        temp = weather_data['main']['temp']
        feels_like = weather_data['main']['feels_like']
        humidity = weather_data['main']['humidity']
        description = weather_data['weather'][0]['description'].title()
        wind_speed = weather_data['wind']['speed']
        
        # Choose emoji based on temperature
        if temp < 0:
            emoji = "🥶"
        elif temp < 10:
            emoji = "❄️"
        elif temp < 20:
            emoji = "🌤️"
        elif temp < 30:
            emoji = "☀️"
        else:
            emoji = "🔥"
        
        # Display results
        print(f"\n{emoji} Weather in {city}, {country}")
        print("=" * 40)
        print(f"🌡️  Temperature:  {temp}°C (Feels like {feels_like}°C)")
        print(f"📝 Conditions:   {description}")
        print(f"💧 Humidity:     {humidity}%")
        print(f"💨 Wind Speed:   {wind_speed} m/s")
        print()

def main():
    """Simple command-line interface"""
    try:
        app = WeatherApp()
    except ValueError as e:
        print(e)
        return
    
    print("🌤️  Simple Weather CLI App")
    print("=" * 30)
    print("Enter city names to get weather info")
    print("Type 'quit' or 'exit' to leave\n")
    
    while True:
        city = input("🏙️  Enter city name: ").strip()
        
        if city.lower() in ['quit', 'exit', 'q']:
            print("👋 Goodbye!")
            break
            
        if not city:
            print("❌ Please enter a valid city name.")
            continue
        
        print(f"🔍 Fetching weather for {city}...")
        weather_data = app.get_weather(city)
        
        if weather_data:
            app.display_weather(weather_data)

if __name__ == "__main__":
    main()