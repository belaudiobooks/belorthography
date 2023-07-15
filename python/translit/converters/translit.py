"""
Basic transliterator interface
"""


class Transliterator:

    def convert(self, text):
        """
        Function responsible for conversion
        :param text: String text to convert
        :return: String conversion result
        """
        raise NotImplementedError("Need to be implemented")

    def meta(self):
        """
        Function must return short descriptor to identify supported
        cases and direction of conversion
        :return: String (ex: 'CYR_NARCOM_TO_CYR')
        """
        raise NotImplementedError("Need to be implemented")
