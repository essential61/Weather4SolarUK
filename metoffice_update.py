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

    # get weather for today
    time_steps = [time_step.text.replace('\r', '').replace('\n', '') for time_step in
                  today_forecast.find_all(class_='time-step-hours')]
    weather_symbols = today_forecast.find_all(class_='weather-symbol-icon')
    today_weather = [(f'{today}T{t} Europe/London', weather_symbols[i].attrs['title']) for i, t in
                    enumerate(time_steps)]

    # open insert file
    insertfilepath = f'forecasts/forecast{today}.sql'
    insert_file_text = ""
    if os.path.exists(insertfilepath):
        with open(insertfilepath, 'r') as insert_file:
            insert_file_text = insert_file.read()
    else:
        sys.exit()

    # open existing update file (if exists)
    updatefilepath = f'forecasts/update{today}.sql'
    old_update_file_text = ""
    if os.path.exists(updatefilepath):
        with open(updatefilepath, 'r') as update_file:
            old_update_file_text = update_file.read()

    # keep any updates in existing update file that have already passed
    old_update_file_text_lines = old_update_file_text.splitlines(keepends = True)
    new_update_file_text = ""
    current_time = time_steps[0].split(':')[0]
    for current_line in old_update_file_text_lines:
        line_time = current_line.split('T')[-1].split(':')[0]
        if line_time >= current_time:
            break
        new_update_file_text += current_line

    # loop through today weather
    for timeperiod in today_weather:
        insert_statement = f'INSERT INTO forecasts (starttime, sky) VALUES (\'{timeperiod[0]}\', \'{timeperiod[1]}\');'
        if insert_statement not in insert_file_text:
            update_statement = f'UPDATE forecasts SET sky = \'{timeperiod[1]}\' WHERE starttime = \'{timeperiod[0]}\'; \n'
            new_update_file_text += update_statement

    # write if changed
    if new_update_file_text != old_update_file_text:
        with open(updatefilepath, 'w') as update_file:
            update_file.write(new_update_file_text)

