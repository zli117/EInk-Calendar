import argparse
import configparser
import os
from configparser import ConfigParser
from typing import List

from google.oauth2.credentials import Credentials

from model.events import GoogleCalendarEvents


class Configurations(object):
    def __init__(self, config: ConfigParser) -> None:
        self._owm_token: str = config.get('API_KEYS', 'OWM', fallback='')
        self._google_token: str = config.get('API_KEYS',
                                             'Google_Token',
                                             fallback='')
        self._google_refresh_token: str = config.get('API_KEYS',
                                                     'Google_Refresh_Token',
                                                     fallback='')
        self._google_client_id: str = config.get('API_KEYS',
                                                 'Google_Client_Id',
                                                 fallback='')
        self._google_client_secrete: str = config.get('API_KEYS',
                                                      'Google_Client_Secrete',
                                                      fallback='')

        self._units: str = config.get('CONFIG', 'Units', fallback='celsius')
        self._city_id: int = config.getint('CONFIG', 'City_Id', fallback=0)
        self._selected_calendars: List[str] = []
        selected_calendars: str = config.get('CONFIG',
                                             'Selected_Calendars',
                                             fallback='')
        for calendar_id in map(lambda s: s.strip(),
                               selected_calendars.split(',')):
            self._selected_calendars.append(calendar_id)

        self._debug_save_path: str = ''
        self._show_borders: bool = False

    @property
    def units(self) -> str:
        return self._units

    @units.setter
    def units(self, units: str) -> None:
        self._units = units

    @property
    def owm_token(self) -> str:
        return self._owm_token

    @owm_token.setter
    def owm_token(self, owm_token: str) -> None:
        self._owm_token = owm_token

    @property
    def google_credentials(self) -> Credentials:
        return Credentials(
            self._google_token,
            refresh_token=self._google_refresh_token,
            client_id=self._google_client_id,
            client_secret=self._google_client_secrete,
            token_uri='https://accounts.google.com/o/oauth2/token')

    @property
    def google_token(self) -> str:
        return self._google_token

    @google_token.setter
    def google_token(self, google_token: str) -> None:
        self._google_token = google_token

    @property
    def google_refresh_token(self) -> str:
        return self._google_refresh_token

    @google_refresh_token.setter
    def google_refresh_token(self, google_refresh_token: str) -> None:
        self._google_refresh_token = google_refresh_token

    @property
    def google_client_id(self) -> str:
        return self._google_client_id

    @google_client_id.setter
    def google_client_id(self, google_client_id: str) -> None:
        self._google_client_id = google_client_id

    @property
    def google_client_secrete(self) -> str:
        return self._google_client_secrete

    @google_client_secrete.setter
    def google_client_secrete(self, google_client_secrete: str) -> None:
        self._google_client_secrete = google_client_secrete

    @property
    def selected_calendars(self) -> List[str]:
        return self._selected_calendars

    @property
    def city_id(self) -> int:
        return self._city_id

    @city_id.setter
    def city_id(self, city_id: int) -> None:
        self._city_id = city_id

    @property
    def is_debug(self) -> bool:
        return len(self._debug_save_path) > 0

    @property
    def debug_save_path(self) -> str:
        return self._debug_save_path

    @debug_save_path.setter
    def debug_save_path(self, path: str) -> None:
        self._debug_save_path = path

    @property
    def show_borders(self) -> bool:
        return self._show_borders

    @show_borders.setter
    def show_borders(self, show_borders: bool) -> None:
        self._show_borders = show_borders

    def add_selected_calendars(self, calendar_id: str) -> None:
        self._selected_calendars.append(calendar_id)

    def save(self, file_path: str) -> None:
        config = configparser.ConfigParser()
        config.add_section('API_KEYS')
        config.set('API_KEYS', 'OWM', self.owm_token)
        config.set('API_KEYS', 'Google_Token', self._google_token)
        config.set('API_KEYS', 'Google_Refresh_Token',
                   self._google_refresh_token)
        config.set('API_KEYS', 'Google_Client_Id', self._google_client_id)
        config.set('API_KEYS', 'Google_Client_Secrete',
                   self._google_client_secrete)

        config.add_section('CONFIG')
        config.set('CONFIG', 'City_Id', str(self.city_id))
        config.set('CONFIG', 'Units', self.units)
        selected_calendars = ','.join(self.selected_calendars)
        config.set('CONFIG', 'Selected_Calendars', selected_calendars)

        with open(file_path, 'w') as file:
            config.write(file)


def load_or_create_config() -> Configurations:
    parser = argparse.ArgumentParser('EInk Smart Calendar')
    parser.add_argument('-c',
                        '--config',
                        type=str,
                        help='Path for the config file')
    parser.add_argument('-d',
                        '--debug',
                        type=str,
                        help='Path for generating debug images')
    parser.add_argument('-s',
                        '--show_border',
                        action='store_true',
                        default=False,
                        help='Path for generating debug images')
    args = parser.parse_args()
    if args.config is not None and os.path.isfile(args.config):
        config = configparser.ConfigParser()
        with open(args.config, 'r') as file:
            config_str = file.read()
            config.read_string(config_str)
        config_obj = Configurations(config)
    else:
        config_obj = Configurations(configparser.ConfigParser())
        config_obj.owm_token = input('Paste in the Open Weather Map Token: \n')
        print('To generate Google API tokens, see the video' +
              ' https://www.youtube.com/watch?v=hfWe1gPCnzc')
        config_obj.google_token = input('Paste in the Access Token: \n')
        config_obj.google_refresh_token = input(
            'Paste in the Refresh Token: \n')
        config_obj.google_client_id = input('Paste in the Client ID: \n')
        config_obj.google_client_secrete = input(
            'Paste in the Client Secrete: \n')

        print('Retrieving calendars ...')
        credentials = config_obj.google_credentials
        google_calendar = GoogleCalendarEvents(credentials)
        list_calendars = google_calendar.list_calendars()
        for i in range(len(list_calendars)):
            print('%d) %s' % (i, list_calendars[i][1]))
        selected_calendars = []
        prompt = ('Select one or more calendars by listing out' +
                  ' their index. Separated by \',\'\n')
        while True:
            selections = input(prompt)
            for index in map(lambda s: s.strip(), selections.split(',')):
                if int(index) >= len(list_calendars):
                    prompt = 'Invalid index. Try again \n'
                    break
                selected_calendars.append(list_calendars[int(index)][0])
            else:
                break
            selected_calendars = []

        for selected_calendar in selected_calendars:
            config_obj.add_selected_calendars(selected_calendar)

        city_id = int(
            input('Paste in the city id for retrieving weather.' +
                  ' The city id could be found on Open Weather' +
                  ' Map website: \n'))
        config_obj.city_id = city_id
        prompt = ('Now select the unit for temperature.' +
                  ' Either "fahrenheit" or "celsius" \n')
        while True:
            units = input(prompt)
            if units != 'fahrenheit' and units != 'celsius':
                prompt = 'Invalid selection. Try again'
            else:
                break

        config_obj.units = units

        saving_path = input('Now provide a path for saving the config \n')

        config_obj.save(saving_path)

        abs_path = os.path.abspath(saving_path)
        print(
            ('Congratulations, configuration is done. The file has been saved'
             + ' to %s. Later runs should specify the arguments:' + ' -c %s') %
            (abs_path, abs_path))

    if args.debug is not None:
        config_obj.debug_save_path = args.debug

    config_obj.show_borders = args.show_border

    return config_obj
