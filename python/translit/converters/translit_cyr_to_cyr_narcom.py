from translit.cases import Case
from translit.converters.translit import Transliterator


class CyrTarasToCyrNar(Transliterator):
    def convert(self, text):
        # TODO: Add implementation instead of stub logic.
        return str(text).lower()

    def meta(self):
        return Case.CYR_TARAS + "_TO_" + Case.CYR_NAR
