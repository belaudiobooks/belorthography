import csv
from dataclasses import dataclass
import json
import pytest
import glob

from belorthography import convert, Case

# List of conversions that we try to test for each test case,
# assuming the test case has text in corresponding cases.
SUPPORTED_CONVERSIONS = (
    (Case.CYR_TARAS, Case.LAT),
    (Case.CYR_NAR, Case.LAT),
    (Case.CYR_TARAS, Case.LAT_NO_DIACTRIC),
    (Case.CYR_NAR, Case.LAT_NO_DIACTRIC),
    (Case.LAT, Case.LAT_NO_DIACTRIC),
)


@dataclass
class TranslationTest:
    name: str
    original_text: str
    expected_text: str
    source_case: Case
    target_case: Case


def convert_test_data_to_cases(
    data: dict[str, str], basename: str
) -> list[TranslationTest]:
    result = []
    for source, target in SUPPORTED_CONVERSIONS:
        original_text = data.get(source.lower(), None)
        expected_text = data.get(target.lower(), None)
        if original_text is None or expected_text is None:
            continue
        result.append(
            TranslationTest(
                name=f"{basename} {source} => {target}",
                original_text=original_text,
                expected_text=expected_text,
                source_case=source,
                target_case=target,
            )
        )
    return result


def read_json_data():
    test_file_list = glob.glob("../tests/*.json")
    all_test_cases: list[TranslationTest] = []
    for test_file in test_file_list:
        with open(test_file) as file:
            test_file_data = json.load(file)
            for test_case in test_file_data["tests"]:
                if test_case.get("disabled", False):
                    continue
                base_name = test_file.split("/")[-1] + "#" + test_case.get("name")
                all_test_cases += convert_test_data_to_cases(test_case, base_name)
    assert len(all_test_cases) > 0
    return all_test_cases


def read_csv_data():
    test_file_list = glob.glob("../tests/*.csv")
    all_test_cases: list[TranslationTest] = []
    for test_file in test_file_list:
        with open(test_file, newline="") as file:
            reader = csv.reader(file)
            header = next(reader)
            line = 2
            for row in reader:
                row_as_dict = {}
                for idx, val in enumerate(row):
                    if val == "":
                        continue
                    row_as_dict[header[idx]] = val
                base_name = test_file.split("/")[-1] + "#" + str(line)
                all_test_cases += convert_test_data_to_cases(row_as_dict, base_name)
                line += 1
    assert len(all_test_cases) > 0
    return all_test_cases


@pytest.mark.parametrize(
    "test_data", read_json_data() + read_csv_data(), ids=lambda data: data.name
)
def test_translate(test_data: TranslationTest):
    actual_text = convert(
        test_data.original_text, test_data.source_case, test_data.target_case
    )
    assert (
        actual_text == test_data.expected_text
    ), f'original text is "{test_data.original_text}", got "{actual_text}" while expected "{test_data.expected_text}"'
