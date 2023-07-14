from translit.cases import Case
from translit.converters.translit import Transliterator


class CyrToCyrNarcom(Transliterator):
    def convert(self, text):
        # TODO: Add implementation instead of stub logic.
        return str(text).lower()

    def meta(self):
        return Case.CYR + "_TO_" + Case.CYR_NARCOM
