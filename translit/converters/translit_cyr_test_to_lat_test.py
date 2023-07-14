from translit.cases import Case
from translit.converters.translit import Transliterator


class CyrTestToLatTest(Transliterator):
    def convert(self, text):
        return str(text).lower()

    def meta(self):
        return Case.CYR_TEST + "_TO_" + Case.LAT_TEST
