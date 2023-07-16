from translit.cases import Case
from translit.converters.translit import Transliterator
from translit.converters.translit_cyr_to_cyr_narcom import CyrTarasToCyrNar
from translit.converters.translit_lat_to_cyr import LatToCyrTaras


class LatToCyrNar(Transliterator):
    def convert(self, text):
        return CyrTarasToCyrNar().convert(LatToCyrTaras().convert(text))

    def meta(self):
        return Case.LAT + "_TO_" + Case.CYR_NAR
