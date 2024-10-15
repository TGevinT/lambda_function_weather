import json
import requests

def lambda_handler(event, context):
    try:
        if isinstance(event, str):
            event = json.loads(event)
        elif isinstance(event, dict) and 'body' in event:
            event = json.loads(event['body'])
        city = event.get('city', 'Unknown City')
    except (ValueError, KeyError, TypeError) as e:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": f"Invalid input: {str(e)}"})
        }
    
    faasd_url = f"http://172.31.88.74:8080/function/weather"
    
    response = requests.post(faasd_url, json={"city": city})
    
    if response.status_code == 200:
        weather_data = response.json()
        temperature_celsius = float(weather_data['temperature'][:-2])
        temperature_fahrenheit = (temperature_celsius * 9/5) + 32
        weather_data['temperature'] = f"{temperature_fahrenheit:.1f}ºF"
        
        # Return hasil akhir
        return {
            "statusCode": 200,
            "body": json.dumps(weather_data)
        }
    else:
        return {
            "statusCode": response.status_code,
            "body": "Error fetching weather data"
        }
