from translit.cases import Case
from translit.converters.translit_cyr_narcom_to_cyr import CyrNarToCyrTaras
from translit.converters.translit_cyr_narcom_to_lat import CyrNarToLat
from translit.converters.translit_cyr_to_cyr_narcom import CyrTarasToCyrNar
from translit.converters.translit_cyr_to_lat import CyrTarasToLat
from translit.converters.translit_lat_to_cyr import LatToCyrTaras
from translit.converters.translit_lat_to_cyr_narcom import LatToCyrNar

"""
Converter map contains lambdas to do not create 
all objects during map initialization
"""
converters = {
    Case.CYR_NAR + "_TO_" + Case.CYR_TARAS: lambda: CyrNarToCyrTaras(),
    Case.CYR_NAR + "_TO_" + Case.LAT: lambda: CyrNarToLat(),
    Case.CYR_TARAS + "_TO_" + Case.LAT: lambda: CyrTarasToLat(),
    Case.CYR_TARAS + "_TO_" + Case.CYR_NAR: lambda: CyrTarasToCyrNar(),
    Case.LAT + "_TO_" + Case.CYR_TARAS: lambda: LatToCyrTaras(),
    Case.LAT + "_TO_" + Case.CYR_TARAS: lambda: LatToCyrNar()
}


def convert(text, source_case, target_case):
    """
    Convert function select implementation based on source and target cases.
    """
    return converters[source_case + '_TO_' + target_case]().convert(text)
