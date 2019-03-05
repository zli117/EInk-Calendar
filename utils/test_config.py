import sys

import pytest

from utils.config_generator import load_or_create_config


@pytest.fixture
def config_no_debug():
    sys.argv.append('-c')
    sys.argv.append('test/test.ini')
    config = load_or_create_config()
    return config


def test_config_no_debug(config_no_debug):
    assert 2 == len(config_no_debug.selected_calendars)
    assert (config_no_debug.selected_calendars[0]
            == config_no_debug.selected_calendars[1])
    assert ('en.usa#holiday@group.v.calendar.google.com'
            == config_no_debug.selected_calendars[0])
    assert 3333333 == config_no_debug.city_id
    assert 'fahrenheit' == config_no_debug.units
    assert 'owm_key' == config_no_debug.owm_token
    assert '123' == config_no_debug.google_credentials.client_secret
    assert '92516' == config_no_debug.google_credentials.client_id
    assert '1/22' == config_no_debug.google_credentials.refresh_token
    assert 'ya29.' == config_no_debug.google_credentials.token
