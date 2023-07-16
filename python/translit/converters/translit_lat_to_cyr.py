from translit.cases import Case
from translit.converters.translit import Transliterator


class LatToCyrTaras(Transliterator):
    def convert(self, text):
        # TODO: Add implementation instead of stub logic.
        return str(text).lower()

    def meta(self):
        return Case.LAT + "_TO_" + Case.CYR_TARAS
