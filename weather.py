from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps

owm = OWM('d53150fe0c97b7dce57b442c043caa46')
mgr = owm.weather_manager()

def get_weather(city):
    try:
        observation = mgr.weather_at_place(f'{city}')
        w = observation.weather
        status = w.detailed_status
        temperature = w.temperature('celsius')
        wind_speed = w.wind()
        rain = w.rain
        humidity = w.humidity  

        data={
            'city': city,
            'status':status,
            'temperature':temperature,
            'wind_speed':wind_speed,
            'rain':rain,
            'humidity':humidity

        }
    except:
        data = None

    return data

# print(get_weather('Tashkent'))

