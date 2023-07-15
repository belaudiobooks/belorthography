from translit.cases import Case
from translit.converters import Transliterator


class CyrNarToCyrTaras(Transliterator):
    def convert(self, text):
        # TODO: Add implementation instead of stub logic.
        return str(text).lower()

    def meta(self):
        return Case.CYR_NAR + "_TO_" + Case.CYR_TARAS
