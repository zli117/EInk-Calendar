import argparse
import configparser
import os

from google.oauth2.credentials import Credentials

from model.events import GoogleCalendarEvents


class Configurations:
    def __init__(self, units: str, owm_token: str,
                 google_credential: Credentials, city_id: int):
        self._units = units
        self._owm_token = owm_token
        self._google_credential = google_credential
        self._selected_calendars = []
        self._city_id = city_id

    @property
    def units(self):
        return self._units

    @units.setter
    def units(self, units: str):
        self._units = units

    @property
    def owm_token(self):
        return self._owm_token

    @owm_token.setter
    def owm_token(self, owm_token: str):
        self._owm_token = owm_token

    @property
    def google_credential(self):
        return self._google_credential

    @property
    def selected_calendars(self):
        return self._selected_calendars

    @property
    def city_id(self):
        return self._city_id

    @city_id.setter
    def city_id(self, city_id: int):
        self._city_id = city_id

    def add_selected_calendars(self, calendar_id: str):
        self._selected_calendars.append(calendar_id)


def load_or_create_config():
    parser = argparse.ArgumentParser('EInk Smart Calendar')
    parser.add_argument('-c', '--config', type=str,
                        help='Path for the config file')
    args = parser.parse_args()
    if args.config is not None and os.path.isfile(args.config):
        config = configparser.ConfigParser()
        with open(args.config, 'r') as file:
            config_str = file.read()
            config.read_string(config_str)

        owm_token = config['API_KEYS']['OWM']
        google_token = config['API_KEYS']['Google_Token']
        google_refresh_token = config['API_KEYS']['Google_Refresh_Token']
        google_client_id = config['API_KEYS']['Google_Client_Id']
        google_client_secrete = config['API_KEYS']['Google_Client_Secrete']
        credentials = Credentials(
            google_token,
            refresh_token=google_refresh_token,
            client_id=google_client_id,
            client_secret=google_client_secrete,
            token_uri='https://accounts.google.com/o/oauth2/token')
        city_id = int(config['CONFIG']['City_Id'])
        units = config['CONFIG']['Units']
        config_obj = Configurations(units, owm_token, credentials, city_id)
        selected_calendars = config['CONFIG']['Selected_Calendars']
        for calendar_id in map(lambda s: s.strip(),
                               selected_calendars.split(',')):
            config_obj.add_selected_calendars(calendar_id)
        return config_obj
    else:
        owm_token = input('Paste in the Open Weather Map Token: \n')
        print('To generate Google API tokens, see the video'
              + ' https://www.youtube.com/watch?v=hfWe1gPCnzc')
        google_token = input('Paste in the Access Token: \n')
        google_refresh_token = input('Paste in the Refresh Token: \n')
        google_client_id = input('Paste in the Client ID: \n')
        google_client_secrete = input('Paste in the Client Secrete: \n')

        print('Retrieving calendars ...')
        credentials = Credentials(
            google_token,
            refresh_token=google_refresh_token,
            client_id=google_client_id,
            client_secret=google_client_secrete,
            token_uri='https://accounts.google.com/o/oauth2/token')
        google_calendar = GoogleCalendarEvents(credentials)
        list_calendars = google_calendar.list_calendars()
        for i in range(len(list_calendars)):
            print('%d) %s' % (i, list_calendars[i][1]))
        selected_calendars = []
        prompt = ('Select one or more calendars by listing out'
                  + ' their index. Separated by \',\'\n')
        while True:
            selections = input(prompt)
            selections = map(lambda s: int(s.strip()), selections.split(','))
            for index in selections:
                if index >= len(list_calendars):
                    prompt = 'Invalid index. Try again \n'
                    break
                selected_calendars.append(list_calendars[index][0])
            else:
                break
            selected_calendars = []

        city_id = int(input('Paste in the city id for retrieving weather.'
                            + ' The city id could be found on Open Weather'
                            + ' Map website: \n'))
        prompt = ('Now select the unit for temperature.'
                  + ' Either "fahrenheit" or "celsius" \n')
        while True:
            units = input(prompt)
            if units != 'fahrenheit' and units != 'celsius':
                prompt = 'Invalid selection. Try again'
            else:
                break

        saving_path = input('Now provide a path for saving the config \n')

        config = configparser.ConfigParser()
        config['API_KEYS'] = {}
        config['API_KEYS']['OWM'] = owm_token
        config['API_KEYS']['Google_Token'] = google_token
        config['API_KEYS']['Google_Refresh_Token'] = google_refresh_token
        config['API_KEYS']['Google_Client_Id'] = google_client_id
        config['API_KEYS']['Google_Client_Secrete'] = google_client_secrete

        config['CONFIG'] = {}
        config['CONFIG']['City_Id'] = str(city_id)
        config['CONFIG']['Units'] = units
        config['CONFIG']['Selected_Calendars'] = ','.join(selected_calendars)

        with open(saving_path, 'w') as file:
            config.write(file)

        abs_path = os.path.abspath(saving_path)
        print(('Congratulations, configuration is done. The file has been saved'
               + ' to %s. Later runs should specify the arguments:'
               + ' -c %s') % (abs_path, abs_path))
        return config
