from flask import Flask, render_template, request
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__, 
           template_folder='templates',
           static_folder='static')
API_KEY = os.getenv('WEATHER_API_KEY')

# Add these lines after creating the Flask app
print("Current working directory:", os.getcwd())
print("Template folder path:", app.template_folder)

@app.route('/', methods=['GET', 'POST'])
def weather():
    weather_data = None
    error = None
    
    if request.method == 'POST':
        city = request.form.get('city')
        if not city:
            error = 'Please enter a city name'
        else:
            try:
                url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
                response = requests.get(url)
                
                if response.status_code == 200:
                    weather_data = response.json()
                else:
                    error = f'City not found. Please check the spelling and try again.'
            except requests.RequestException as e:
                error = f'Error fetching weather data: {str(e)}'
    
    return render_template('weather.html', weather_data=weather_data, error=error)

@app.route('/forecast/<city>')
def forecast(city):
    try:
        url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric'
        response = requests.get(url)
        if response.status_code == 200:
            forecast_data = response.json()
            return render_template('forecast.html', forecast_data=forecast_data)
        else:
            return 'Error fetching forecast data', 400
    except requests.RequestException as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=True) 