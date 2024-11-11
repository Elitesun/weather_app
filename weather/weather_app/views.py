from django.conf import settings
import requests
from django.views import View
from django.shortcuts import render
from datetime import datetime

# Define a view class for handling weather data
class WeatherView(View):
    def get(self, request):
        
        # Retrieve the API key from settings
        api_key = settings.OPENWEATHER_API_KEY
        # Get the city from the request query parameters, default to 'New York' if not provided
        city = request.GET.get('city',' New York')  
        # Construct the URL for the current weather data
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
        
        # Construct the URL for the forecast data
        forecast_url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric'
        
        # Send a GET request to the forecast API
        forecast_response=requests.get(forecast_url)
        
        # Parse the JSON response from the forecast API
        forecast_data=forecast_response.json()
        
        
        # Send a GET request to the current weather API
        response = requests.get(url)
        # Parse the JSON response from the current weather API
        weather_data = response.json()
        # Extract the icon code from the weather data
        icon_code = weather_data['weather'][0]['icon']
        # Construct the URL for the icon image
        icon_url = f'http://openweathermap.org/img/wn/{icon_code}@2x.png'  # URL for the icon image


        # Check if the response was successful
        if response.status_code == 200:
            # Prepare the weather data for rendering
            weather = {
                'city': weather_data['name'],
                'temperature': f"{weather_data['main']['temp']}°C",
                'description': weather_data['weather'][0]['description'],
                "humidity": f"{weather_data['main']['humidity']}%",
                "wind_speed":f"{weather_data['wind']['speed']} m/s",
                'icon_url': icon_url,
                
                'date': datetime.now().strftime("%A %d %b") 
            }
        else:
            # Prepare default weather data if the response was not successful
            weather = {
                'city': city,
                'temperature': 'N/A',
                'description': 'Weather data not available',
                'humidity': 'N/A',
                'wind_speed': 'N/A',
                'icon_url': '❓',
                'date' : 'N/A'
            }
            


        # Initialize an empty list to hold forecast data
        forecast_list=[]
        # Check if the forecast response was successful
        if forecast_response.status_code==200:
            # Parse the forecast data
            forecast_data = forecast_response.json()
            # Loop through the first 6 forecast entries
            for forecast in forecast_data.get('list', [])[:6]:
                # Prepare each forecast entry for rendering
                forecast_list.append({
                'date_time' : forecast.get('dt_txt'),
                'temperature' : f"{forecast['main'].get('temp' , 'N/A')}°C",
                'description': forecast['weather'][0].get('description', 'No description available'),
                'humidity' : f"{forecast['main'].get('humidity','N/A')}%",
                'wind_speed' : f"{forecast['wind'].get('speed' ,'N/A')} m/s",
                })
        else:
            # Log a message if the forecast data is not available
            print("Forecast data not available.")

        # Render the weather template with the prepared weather and forecast data
        return render(request, 'weather.html', {'weather': weather,
                                                'forecast' : forecast_list})

