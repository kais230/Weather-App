from django.shortcuts import render
import requests
from datetime import datetime

def is_numeric(string):
    try:
        float_value = float(string)
        return True
    except ValueError:
        return False


def index(request):
    api_key = '70f7385751c94f9e91b124150241802'

    if request.method == 'POST':
        city = request.POST['city']
        forecast_url =f'http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city}&days=4&aqi=no&alerts=no'

        if not city or is_numeric(city):
            error_message = "Please enter a city name."
            context = {
                'error_message': error_message,
            }
            return render(request, 'weather_app/index.html', context)

        weather_data1, error_message = fetch_weather(city, api_key, forecast_url)
        forecast_data1, error_message = fetch_forecast(city, api_key, forecast_url)

        context = {
            'weather_data1': weather_data1,
            'forecast_data1': forecast_data1,
            'error_message': error_message,
        }

        return render(request, 'weather_app/index.html', context)
    else:
        return render(request, 'weather_app/index.html')


def fetch_weather(city, api_key, current_weather_url):
    response = requests.get(current_weather_url.format(api_key, city)).json()

    if 'error' in response:
        error_message = "City not found. Please enter a valid city name."
        return None, error_message

    date_object = datetime.strptime(response['forecast']['forecastday'][0]['date'], "%Y-%m-%d")

    weather_data = {
        'city': response['location']['name'],
        'country': response['location']['country'],
        'temperature': round(response['current']['temp_c']),
        'feels_like_temperature': round(response['current']['feelslike_c']),
        'wind': response['current']['wind_kph'],
        'description': response['current']['condition']['text'],
        'icon': response['current']['condition']['icon'],
        'date': date_object.strftime("%A, %d %B %Y"),
        'min_temp': round(response['forecast']['forecastday'][0]['day']['mintemp_c']),
        'max_temp': round(response['forecast']['forecastday'][0]['day']['maxtemp_c']),
        'sunrise': response['forecast']['forecastday'][0]['astro']['sunrise'],
        'sunset': response['forecast']['forecastday'][0]['astro']['sunset'],
        'chance_of_rain': response['forecast']['forecastday'][0]['day']['daily_chance_of_rain']

    }

    return weather_data, None


def fetch_forecast(city, api_key, forecast_url):
    forecast_response = requests.get(forecast_url.format(api_key, city)).json()
    if 'error' in forecast_response:
        error_message = "City not found. Please enter a valid city name."
        return None, error_message

    daily_forecasts = []
    first_iteration = True
    for daily_data in forecast_response['forecast']['forecastday']:
        if first_iteration:
            first_iteration = False
            continue  # Skip the first iteration

        date_object = datetime.strptime(daily_data['date'], "%Y-%m-%d")
        daily_forecasts.append({
            'date': date_object.strftime("%A, %d %B %Y"),
            'min_temp': round(daily_data['day']['mintemp_c']),
            'max_temp': round(daily_data['day']['maxtemp_c']),
            'description': daily_data['day']['condition']['text'],
            'icon': daily_data['day']['condition']['icon'],
            'chance_of_rain': daily_data['day']['daily_chance_of_rain'],
            'sunrise': daily_data['astro']['sunrise'],
            'sunset': daily_data['astro']['sunset'],
        })

    return daily_forecasts, None




