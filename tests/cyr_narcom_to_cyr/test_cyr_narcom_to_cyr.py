import json
import pytest
import glob

from translit import convert
from translit.cases import Case


def read_json_data():
    test_file_list = glob.glob('tests/cyr_narcom_to_cyr/test_cases/test_*.json')
    all_test_cases = []
    for test_file in test_file_list:
        with open(test_file) as file:
            test_file_data = json.load(file)
        all_test_cases += test_file_data['tests']
    return all_test_cases


@pytest.mark.parametrize("test_data", read_json_data(), ids=lambda data: data['name'])
def test_translate(test_data):
    assert convert(test_data['input'], Case.CYR, Case.CYR_NARCOM) == test_data['expected_output']

