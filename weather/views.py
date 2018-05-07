from django.shortcuts import render
import requests
from weather.models import City
from weather.forms import CityForm

#TODO: Move to dot env

WEATHER_URL='http://samples.openweathermap.org/data/2.5/weather?q={}&appid=b6907d289e10d714a6e88b30761fae22'

ON = 'on'
OFF = 'off'

FAHR='F'
CELS='C'

def index(request):

    cities = City.objects.all()

    enable_celcius = OFF  # Value is fahrenheit Default
    degree = FAHR  # Value is fahrenheit Default

    if request.method == 'POST':  # only true if form is submitted
        enable_celcius = request.POST.get('C', '')
        form = CityForm(request.POST)  # add actual request data to form for processing
        form.save()

    weather_data = []

    for city in cities:
        # TODO: HTTPConnectionPool Exception
        city_weather = requests.get(WEATHER_URL.format(city)).json()

        temp_degree = city_weather['main']['temp']

        if enable_celcius == ON:
            far = city_weather['main']['temp']
            celcius = ((far - 32) * 5) / 9
            temp_degree = "%.2f" % celcius  # Limiting float to two decimal points
            degree = CELS

        weather = {
            'city': city,
            'temperature': temp_degree,
            'degree': degree,
            'description': city_weather['weather'][0]['description'],
            'icon': city_weather['weather'][0]['icon']
        }

        weather_data.append(weather)

    context = {'weather_data': weather_data}

    return render(request, 'weather/index.html', context)

