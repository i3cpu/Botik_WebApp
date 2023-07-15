from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps

owm = OWM('d53150fe0c97b7dce57b442c043caa46')
mgr = owm.weather_manager()


# Search for current weather in London (Great Britain) and get details
observation = mgr.weather_at_place('London,GB')
w = observation.weather

status = w.detailed_status         # 'clouds'
wind_speed = w.wind()                  # {'speed': 4.6, 'deg': 330}
temp = w.temperature('celsius')  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}
rain = w.rain                    # {}
# w.humidity                # 87
# w.heat_index              # None
# w.clouds                  # 75


print(t)