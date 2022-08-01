import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm

def index(request):
    appid = 'a5dc1a83a554d64e8bd2235c4ff3b7c7'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + appid

    if (request.method == 'POST'):
        form = CityForm(request.POST)
        form.save()

    form = CityForm()

    cities = City.objects.all()                             

    all_cities = [] 
    last_cities = []                                       
    

    for city in cities:
        res = requests.get(url.format(city.name)).json()
        city_info = {
            'city': city.name,
            'temp': res['main']['temp'],
            'humidity': res['main']['humidity'],
            'pressure': res['main']['pressure'],
            'feels_like': res['main']['feels_like'],
            'icon': res['weather'][0]['icon'],
            'wind': res['wind']['speed'],
            'clouds': res['clouds']['all'],
            'visibility': res['visibility']
            }

        if len(all_cities) <= 4:
            all_cities.insert(0, city_info)
            last_cities = city_info
        else:
            all_cities.insert(0, city_info)
            all_cities.pop(-1)
            last_cities = city_info
        

    context = {
        'all_info': all_cities,
        'last_info': last_cities,
        'form': form,
    }

    return render(request, 'weather/index.html', context)
