from translit.cases import Case
from translit.converters import Transliterator
from translit.converters.translit_cyr_narcom_to_cyr import CyrNarToCyrTaras
from translit.converters.translit_cyr_to_lat import CyrTarasToLat


class CyrNarToLat(Transliterator):
    def convert(self, text):
        return CyrTarasToLat().convert(CyrNarToCyrTaras().convert(text))

    def meta(self):
        return Case.CYR_NAR + "_TO_" + Case.LAT
