import json
import pytest

from translit import convert
from translit.cases import Case


def read_json_data():
    with open('tests/cyr_test_to_lat_test/test1.json') as file:
        data = json.load(file)
    return data['tests']


@pytest.mark.parametrize("test_data", read_json_data(), ids=lambda data: data['name'])
def test_translate(test_data):
    assert convert(test_data['input'], Case.CYR_TEST, Case.LAT_TEST) == test_data['expected_output']
