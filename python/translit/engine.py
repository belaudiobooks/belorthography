from translit.cases import Case
from translit.converters import translit_cyr_taras_to_lat, translit_cyr_nar_to_lat

from collections.abc import Callable, Mapping

"""
Converter functions map
"""
converters: Mapping[str, Callable[[str], str]] = {
    Case.CYR_TARAS + "_TO_" + Case.LAT: translit_cyr_taras_to_lat.convert,
    Case.CYR_NAR + "_TO_" + Case.LAT: translit_cyr_nar_to_lat.convert,
}

def convert(text, source_case, target_case):
    """
    Convert function select implementation based on source and target cases.
    """
    return converters[source_case + '_TO_' + target_case](text)
