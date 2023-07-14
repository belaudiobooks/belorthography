from translit.converters.translit_cyr_test_to_lat_test import CyrTestToLatTest

converters = {
    'CYR_TEST_TO_LAT_TEST': lambda: CyrTestToLatTest(),
}


def convert(text, source_case, target_case):
    """
    Convert function select implementation based of source and target case.
    """
    return converters[source_case + '_TO_' + target_case]().convert(text)
