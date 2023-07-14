from translit.cases import Case
from translit.converters.translit import Transliterator


class CyrNarcomToCyr(Transliterator):
    def convert(self, text):
        # TODO: Add implementation instead of stub logic.
        return str(text).lower()

    def meta(self):
        return Case.CYR_NARCOM + "_TO_" + Case.CYR
