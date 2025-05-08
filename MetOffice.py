# Imports.
import sys
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# The script starts here.
if __name__ == '__main__':
    # run as 'python MetOffice.py <place_code>'
    # Use the place_code value for your location
    # To find your place code, look at the url of the search result for your location returned from https://www.metoffice.gov.uk/
    # i.e. https://weather.metoffice.gov.uk/forecast /{place_code}?date=YYYY-mm-dd
    place_code = sys.argv[1]
    url = f'https://weather.metoffice.gov.uk/forecast/{place_code}'
    met_response = requests.get(url)
    met_html = BeautifulSoup(met_response.content, 'html.parser')
    today = datetime.today()
    tomorrow = (today + timedelta(1)).strftime('%Y-%m-%d')
    tomorrow_forecast = met_html.find('div', id=tomorrow)
    time_steps = [time_step.text.replace('\r', '').replace('\n', '') for time_step in
                  tomorrow_forecast.find_all(class_='time-step-hours')]
    weather_symbols = tomorrow_forecast.find_all(class_='weather-symbol-icon')
    tomorrow_weather = [(f'{tomorrow}T{t} Europe/London', weather_symbols[i].attrs['title']) for i, t in
                    enumerate(time_steps)]
    with open(f'forecasts/forecast{tomorrow}.sql', 'w') as file_handler:
        file_handler.write(f'-- created {today}\n')
        for timeperiod in tomorrow_weather:
            file_handler.write(f'INSERT INTO forecasts (starttime, sky) VALUES (\'{timeperiod[0]}\', \'{timeperiod[1]}\');\n')
