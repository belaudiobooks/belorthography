from translit.cases import Case
from translit.converters.translit import Transliterator
from translit.converters.translit_cyr_narcom_to_cyr import CyrNarcomToCyr
from translit.converters.translit_cyr_to_lat import CyrToLat


class CyrNarcomToLat(Transliterator):
    def convert(self, text):
        return CyrToLat().convert(CyrNarcomToCyr().convert(text))

    def meta(self):
        return Case.CYR_NARCOM + "_TO_" + Case.LAT
