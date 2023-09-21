import json
import pytest
import glob

from belorthography import convert, Case


def read_json_data():
    test_file_list = glob.glob("../tests/*.json")
    all_test_cases = []
    for test_file in test_file_list:
        with open(test_file) as file:
            test_file_data = json.load(file)
            for test_case in test_file_data["tests"]:
                if test_case.get("disabled", False):
                    continue
                test_case["name"] = (
                    test_file.split("/")[-1] + "#" + test_case.get("name")
                )
                all_test_cases.append(test_case)
    return all_test_cases


@pytest.mark.parametrize("test_data", read_json_data(), ids=lambda data: data["name"])
def test_translate(test_data):
    if "cyr_taras" in test_data:
        converted = convert(
            test_data["cyr_taras"],
            Case.CYR_TARAS,
            Case.LAT,
        )
        assert converted == test_data["lat"]
    if "cyr_nar" in test_data:
        converted = convert(
            test_data["cyr_nar"],
            Case.CYR_NAR,
            Case.LAT,
        )
        assert converted == test_data["lat"]
