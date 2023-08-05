# weather_app/views.py

import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

def weather_app_home(request):
    return render(request, 'index.html')


def get_weather_data_from_external_api(location):
    api_base_url = 'https://api.openweathermap.org/data/2.5/weather'
    api_key = '64c5ca944c5abc9d967e45868797826b'  # Replace this with your actual API key from OpenWeatherMap

    params = {
        'q': location,
        'appid': api_key,
    }

    response = requests.get(api_base_url, params=params)
    data = response.json()

    if response.status_code == 200:
        try:
            # Extract relevant weather information from the API response
            weather_data = {
                'location': location,
                'temperature': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'description': data['weather'][0]['description'],
            }
            return weather_data
        except KeyError:
            # Handle missing keys or incorrect data structure
            return {'error': 'Invalid API response format'}
    else:
        # Handle non-200 status codes (e.g., API errors)
        return {'error': 'Weather API error'}

    return weather_data

@csrf_exempt
def get_weather(request):
    if request.method == 'POST':
        location = request.POST.get('location')

        # Fetch weather data from the external API
        weather_data = get_weather_data_from_external_api(location)

        # Return weather data as a JSON response
        return JsonResponse(weather_data)
    

def get_available_cities(request):
    search_value = request.GET.get('search', '')

    # Replace 'your-api-key' with the actual API key from the weather API provider
    api_key = '64c5ca944c5abc9d967e45868797826b'
    api_base_url = 'https://api.openweathermap.org/data/2.5/find'
    params = {
        'q': search_value,
        'type': 'like',
        'appid': api_key,
    }

    response = requests.get(api_base_url, params=params)
    data = response.json()

    if 'list' in data:
        cities = [{'name': city['name'], 'country': city['sys']['country']} for city in data['list']]
    else:
        cities = []

    return JsonResponse(cities, safe=False)