# Imports.
import os
import sys
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# The script starts here.
if __name__ == '__main__':
    # run as 'python metoffice_update.py <place_code>'
    # Use the place_code value for your location
    # To find your place code, look at the url of the search result for your location returned from https://www.metoffice.gov.uk/
    # i.e. https://weather.metoffice.gov.uk/forecast /{place_code}?date=YYYY-mm-dd
    place_code = sys.argv[1]
    url = f'https://weather.metoffice.gov.uk/forecast/{place_code}'
    met_response = requests.get(url)
    met_html = BeautifulSoup(met_response.content, 'html.parser')
    today = datetime.today().strftime('%Y-%m-%d')
    today_forecast = met_html.find('div', id=today)
    # weather for next hour
    next_hour = f'{today}T{today_forecast.find(class_='time-step-hours').text} Europe/London'
    next_weather = today_forecast.find(class_='weather-symbol-icon').attrs['title']
    insert_statement = f'INSERT INTO forecasts (starttime, sky) VALUES (\'{next_hour}\', \'{next_weather}\');'
    insertfilepath = f'forecasts/forecast{today}.sql'
    if os.path.exists(insertfilepath):
        with open(f'forecasts/forecast{today}.sql', 'r') as insert_file:
            insert_file_text = insert_file.read()
        if insert_statement not in insert_file_text:
            update_statement = f'UPDATE forecasts SET sky = \'{next_weather}\' WHERE starttime = \'{next_hour}\';'
            with open(f'forecasts/update{today}.sql', 'a') as update_file:
                update_file.write(f'{update_statement}\n')
