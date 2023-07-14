from translit.cases import Case
from translit.converters.translit import Transliterator
from translit.converters.translit_cyr_to_cyr_narcom import CyrToCyrNarcom
from translit.converters.translit_lat_to_cyr import LatToCyr


class LatToCyrNarcom(Transliterator):
    def convert(self, text):
        return CyrToCyrNarcom().convert(LatToCyr().convert(text))

    def meta(self):
        return Case.LAT + "_TO_" + Case.CYR_NARCOM
