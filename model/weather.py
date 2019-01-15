import datetime

from pyowm import OWM


class OpenWeatherMapModel:
    def __init__(self, api_key: str, city_id: int):
        self.owm = OWM(api_key)
        self._city_id = city_id
        self._unit = 'celsius'

    @property
    def city_id(self):
        return self._city_id

    @city_id.setter
    def city_id(self, city_id: int):
        self._city_id = city_id

    @property
    def temperature_unit(self):
        return self._unit

    @temperature_unit.setter
    def temperature_unit(self, unit: str):
        assert unit == 'fahrenheit' or unit == 'celsius'
        self._unit = unit

    def _parse_weather(self, weather):
        temperature = weather.get_temperature(unit=self.temperature_unit)
        humidity = weather.get_humidity()
        weather_code = weather.get_weather_code()
        return (weather_code,
                temperature.get('temp_min', temperature.get('min')),
                temperature.get('temp_max', temperature.get('max')),
                humidity)

    def get_current_weather(self):
        """
        Get the current weather data
        :return: Tuple of weather code, temperature range, and humidity
        """
        obs = self.owm.weather_at_id(self.city_id)
        weather = obs.get_weather()
        return self._parse_weather(weather)

    def get_daily_forecast(self, limit=14, include_today=False):
        """
        Get a list of forecasts
        :param limit: The max number of forecasts to get
        :param include_today: whether include today in the forecast
        :return: list of tuples of weather code, temperature range and humidity
        """
        forecaster = self.owm.daily_forecast_at_id(self.city_id, limit=limit)
        weathers = forecaster.get_forecast().get_weathers()
        today = datetime.datetime.now().date()
        if not include_today:
            weathers = filter(lambda weather: not (
                    weather.get_reference_time(timeformat='date') == today),
                              weathers)
        return list(map(lambda weather: self._parse_weather(weather), weathers))
