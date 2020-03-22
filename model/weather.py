import datetime
from typing import List, Tuple

from pyowm import OWM
from pyowm.weatherapi25.weather import Weather


class OpenWeatherMapModel(object):
    def __init__(self, api_key: str, city_id: int) -> None:
        self.owm = OWM(api_key)
        self._city_id = city_id
        self._unit = 'celsius'
        self._current_weather = (0, 0.0, 0.0, 0.0, 0.0)
        self._forecast: List[Tuple[int, float, float, float, float]] = []

    @property
    def city_id(self) -> int:
        return self._city_id

    @city_id.setter
    def city_id(self, city_id: int) -> None:
        self._city_id = city_id

    @property
    def temperature_unit(self) -> str:
        return self._unit

    @temperature_unit.setter
    def temperature_unit(self, unit: str) -> None:
        assert unit == 'fahrenheit' or unit == 'celsius'
        self._unit = unit

    def _parse_weather(
            self, weather: Weather) -> Tuple[int, float, float, float, float]:
        temperature = weather.get_temperature(unit=self.temperature_unit)
        humidity = weather.get_humidity()
        weather_code = weather.get_weather_code()
        return (weather_code,
                temperature.get('temp_min', temperature.get('min')),
                temperature.get('temp_max', temperature.get('max')),
                temperature.get('temp'), humidity)

    def get_current_weather(self) -> Tuple[int, float, float, float, float]:
        """
        Get the current weather data
        :return: Tuple of weather code, temperature range, current temperature
                 and humidity
        """
        try:
            obs = self.owm.weather_at_id(self.city_id)
            weather = obs.get_weather()
            self._current_weather = self._parse_weather(weather)
        except Exception as exception:
            print(exception)
        return self._current_weather

    def get_daily_forecast(
        self,
        limit: int = 14,
        include_today: bool = False
    ) -> List[Tuple[int, float, float, float, float]]:
        """
        Get a list of forecasts
        :param limit: The max number of forecasts to get
        :param include_today: whether include today in the forecast
        :return: list of tuples of weather code, temperature range, temperature
                 and humidity
        """
        try:
            forecaster = self.owm.daily_forecast_at_id(self.city_id,
                                                       limit=limit)
            weathers = forecaster.get_forecast().get_weathers()
            today = datetime.datetime.now().date()
            if not include_today:
                weathers = filter(
                    lambda weather: not (weather.get_reference_time(
                        timeformat='date').date() == today), weathers)
            self._forecast = list(
                map(lambda weather: self._parse_weather(weather), weathers))
        except Exception as exception:
            print(exception)
        return self._forecast
