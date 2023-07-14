from translit.cases import Case
from translit.converters.translit_cyr_narcom_to_cyr import CyrNarcomToCyr
from translit.converters.translit_cyr_narcom_to_lat import CyrNarcomToLat
from translit.converters.translit_cyr_to_cyr_narcom import CyrToCyrNarcom
from translit.converters.translit_cyr_to_lat import CyrToLat
from translit.converters.translit_lat_to_cyr import LatToCyr
from translit.converters.translit_lat_to_cyr_narcom import LatToCyrNarcom

"""
Converter map contains lambdas to do not create 
all objects during map initialization
"""
converters = {
    Case.CYR_NARCOM + "_TO_" + Case.CYR: lambda: CyrNarcomToCyr(),
    Case.CYR_NARCOM + "_TO_" + Case.LAT: lambda: CyrNarcomToLat(),
    Case.CYR + "_TO_" + Case.LAT: lambda: CyrToLat(),
    Case.CYR + "_TO_" + Case.CYR_NARCOM: lambda: CyrToCyrNarcom(),
    Case.LAT + "_TO_" + Case.CYR: lambda: LatToCyr(),
    Case.LAT + "_TO_" + Case.CYR: lambda: LatToCyrNarcom()
}


def convert(text, source_case, target_case):
    """
    Convert function select implementation based on source and target cases.
    """
    return converters[source_case + '_TO_' + target_case]().convert(text)
