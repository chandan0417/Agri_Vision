import os
from flask import Flask, redirect, render_template, request, jsonify
from PIL import Image
from werkzeug.utils import secure_filename
from thermal_processor import ThermalImageProcessor
import torchvision.transforms.functional as TF
import CNN
import numpy as np
import torch
import pandas as pd
import requests

def load_supplement_data():
    return pd.read_csv('supplement_info.csv', encoding='cp1252')

disease_info = pd.read_csv('disease_info.csv', encoding='cp1252')
supplement_info = load_supplement_data()

model = CNN.CNN(39)    
model.load_state_dict(torch.load("plant_disease_model_1_latest.pt"))
model.eval()

def prediction(image_path):
    image = Image.open(image_path)
    image = image.resize((224, 224))
    input_data = TF.to_tensor(image)
    input_data = input_data.view((-1, 3, 224, 224))
    output = model(input_data)
    output = output.detach().numpy()
    index = np.argmax(output)
    return index


from weather_api import weather_api_bp

app = Flask(__name__)

app.register_blueprint(weather_api_bp)

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/contact')
def contact():
    return render_template('contact-us.html')

@app.route('/index')
def ai_engine_page():
    return render_template('index.html')

@app.route('/mobile-device')
def mobile_device_detected_page():
    return render_template('mobile-device.html')

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        image = request.files['image']
        filename = image.filename
        file_path = os.path.join('static/uploads', filename)
        image.save(file_path)
        print(file_path)
        pred = prediction(file_path)
        title = disease_info['disease_name'][pred]
        description =disease_info['description'][pred]
        prevent = disease_info['Possible Steps'][pred]
        image_url = disease_info['image_url'][pred]
        supplement_name = supplement_info['supplement name'][pred]
        supplement_image_url = supplement_info['supplement image'][pred]
        supplement_buy_link = supplement_info['buy link'][pred]
        return render_template('submit.html' , title = title , desc = description , prevent = prevent , 
                               image_url = image_url , pred = pred ,sname = supplement_name , simage = supplement_image_url , buy_link = supplement_buy_link)

@app.route('/market', methods=['GET', 'POST'])
def market():
    return render_template('market.html', supplement_image = list(supplement_info['supplement image']),
                           supplement_name = list(supplement_info['supplement name']), disease = list(disease_info['disease_name']), buy = list(supplement_info['buy link']))

@app.route('/irrigation')
def irrigation():
    return render_template('irrigation.html')

@app.route('/analyze_thermal', methods=['POST'])
def analyze_thermal():
    if 'image' not in request.files:
        return jsonify({'success': False, 'error': 'No image uploaded'})
    
    image = request.files['image']
    if image.filename == '':
        return jsonify({'success': False, 'error': 'No image selected'})

    try:
        # Create uploads directory if it doesn't exist
        upload_dir = os.path.join('static', 'uploads')
        thermal_dir = os.path.join('static', 'thermal')
        os.makedirs(upload_dir, exist_ok=True)
        os.makedirs(thermal_dir, exist_ok=True)

        # Save original image
        filename = secure_filename(image.filename)
        original_path = os.path.join(upload_dir, filename)
        image.save(original_path)

        # Process the image
        processor = ThermalImageProcessor()
        
        # Generate thermal image and get analysis
        thermal_filename = f'thermal_{filename}'
        thermal_path = os.path.join(thermal_dir, thermal_filename)
        
        # Process image and get results
        results = processor.process_image(original_path, colormap='thermal', save_path=thermal_path)

        return jsonify({
            'success': True,
            'original_image': f'/static/uploads/{filename}',
            'thermal_image': f'/static/thermal/{thermal_filename}',
            'moisture_levels': results['moisture_levels'],
            'recommendations': results['recommendations']
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/refresh_data')
def refresh_data():
    global supplement_info
    supplement_info = load_supplement_data()
    return jsonify({'success': True, 'message': 'Data refreshed'})

@app.route('/weather')
def weather():
    return render_template('weather.html')

@app.route('/weather_api')
def weather_api():
    from flask import jsonify
    import requests

    lat = request.args.get('lat')
    lon = request.args.get('lon')

    # You'll need to replace this with your actual API key
    api_key = request.args.get('api_key', 'fafe541c895752f3ab410f8a51c6c040')

    # Validate inputs
    if not lat or not lon:
        return jsonify({
            'success': False,
            'error': 'Latitude and longitude are required'
        })

    # Use OpenWeatherMap One Call API to get current weather and 7-day forecast
    onecall_url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&appid={api_key}&units=metric&exclude=minutely,hourly,alerts"

    try:
        response = requests.get(onecall_url, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Extract location name and country using reverse geocoding API (optional)
        # For simplicity, use lat/lon as coordinates string
        location_name = f"Lat: {lat}, Lon: {lon}"
        country = ""

        current_data = data.get('current', {})
        daily_data = data.get('daily', [])

        # Extract current weather info
        current_temp = current_data.get('temp', 0)
        current_feels_like = current_data.get('feels_like', 0)
        current_humidity = current_data.get('humidity', 0)
        current_pressure = current_data.get('pressure', 0)
        current_weather = current_data.get('weather', [{}])[0]
        current_condition = current_weather.get('main', '')
        current_description = current_weather.get('description', '')
        current_icon = current_weather.get('icon', '')
        wind_speed = current_data.get('wind_speed', 0)
        wind_direction = current_data.get('wind_deg', 0)
        sunrise = current_data.get('sunrise', 0)
        sunset = current_data.get('sunset', 0)

        # Extract daily forecast for 7 days
        daily_forecast = []
        for day in daily_data[:7]:
            weather = day.get('weather', [{}])[0]
            daily_forecast.append({
                'dt': day.get('dt', 0),
                'temp_day': day.get('temp', {}).get('day', 0),
                'temp_min': day.get('temp', {}).get('min', 0),
                'temp_max': day.get('temp', {}).get('max', 0),
                'humidity': day.get('humidity', 0),
                'condition': weather.get('main', ''),
                'description': weather.get('description', ''),
                'icon': weather.get('icon', ''),
                'wind_speed': day.get('wind_speed', 0),
                'pop': day.get('pop', 0) * 100  # Probability of precipitation (as percentage)
            })

        return jsonify({
            'success': True,
            'location': location_name if location_name else '',
            'coordinates': f"Lat: {lat}, Lon: {lon}",
            'current': {
                'temp': round(current_temp, 1),
                'feels_like': round(current_feels_like, 1),
                'condition': current_condition,
                'description': current_description,
                'icon': current_icon,
                'humidity': current_humidity,
                'pressure': current_pressure,
                'wind_speed': wind_speed,
                'wind_direction': wind_direction,
                'sunrise': sunrise,
                'sunset': sunset
            },
            'forecast': daily_forecast
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    app.run(debug=True)
