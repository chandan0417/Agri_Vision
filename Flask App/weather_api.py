from flask import Blueprint, request, jsonify
import requests
from datetime import datetime

weather_api_bp = Blueprint('weather_api_bp', __name__)

@weather_api_bp.route('/weather_api')
def weather_api():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    location = request.args.get('location')
    
    # API key
    api_key = 'fafe541c895752f3ab410f8a51c6c040'

    # If location is provided, use geocoding API to get lat/lon
    if location:
        geocode_url = f"http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=1&appid={api_key}"
        try:
            geocode_response = requests.get(geocode_url, timeout=10)
            geocode_response.raise_for_status()
            geocode_data = geocode_response.json()
            if not geocode_data:
                return jsonify({
                    'success': False,
                    'error': f'Location \"{location}\" not found'
                })
            lat = geocode_data[0]['lat']
            lon = geocode_data[0]['lon']
        except requests.exceptions.RequestException as e:
            return jsonify({
                'success': False,
                'error': f'Geocoding API error: {str(e)}'
            })

    if not lat or not lon:
        return jsonify({
            'success': False,
            'error': 'Latitude and longitude are required'
        })

    try:
        # Get current weather
        current_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        current_response = requests.get(current_url, timeout=10)
        current_response.raise_for_status()
        current_data = current_response.json()

        # Get 5-day forecast (this is the maximum in free tier)
        forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        forecast_response = requests.get(forecast_url, timeout=10)
        forecast_response.raise_for_status()
        forecast_data = forecast_response.json()

        # Process current weather
        current_weather = {
            'temp': round(current_data['main']['temp'], 1),
            'feels_like': round(current_data['main']['feels_like'], 1),
            'humidity': current_data['main']['humidity'],
            'pressure': current_data['main']['pressure'],
            'wind_speed': current_data['wind']['speed'],
            'description': current_data['weather'][0]['description'].capitalize(),
            'icon': current_data['weather'][0]['icon'],
            'location': current_data['name'] + ', ' + current_data.get('sys', {}).get('country', '')
        }

        # Process forecast (get one reading per day)
        daily_forecast = []
        used_dates = set()
        
        for item in forecast_data['list']:
            date = datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')
            
            if date not in used_dates:
                used_dates.add(date)
                daily_forecast.append({
                    'date': datetime.fromtimestamp(item['dt']).strftime('%A, %b %d'),
                    'temp_max': round(item['main']['temp_max'], 1),
                    'temp_min': round(item['main']['temp_min'], 1),
                    'humidity': item['main']['humidity'],
                    'description': item['weather'][0]['description'].capitalize(),
                    'icon': item['weather'][0]['icon'],
                    'wind_speed': item['wind']['speed']
                })

                if len(daily_forecast) >= 5:  # We only need 5 days
                    break

        return jsonify({
            'success': True,
            'current': current_weather,
            'forecast': daily_forecast
        })

    except requests.exceptions.RequestException as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'An unexpected error occurred'
        })
