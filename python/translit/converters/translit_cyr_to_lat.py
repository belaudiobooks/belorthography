from translit.cases import Case
from translit.converters.translit import Transliterator


class CyrTarasToLat(Transliterator):
    def convert(self, text):
        # TODO: Add implementation instead of stub logic.
        return str(text).lower()

    def meta(self):
        return Case.CYR_TARAS + "_TO_" + Case.LAT
