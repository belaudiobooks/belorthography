"""
Class mimic to enum to keep consistent definition
all possible transliteration case options.
"""


class Orthography:
    """
    Also known as Taraškievica
    https://en.wikipedia.org/wiki/Tara%C5%A1kievica
    """
    CLASSICAL = "CLASSICAL"

    """
    Also known as Narkamaŭka
    https://en.wikipedia.org/wiki/Narkama%C5%ADka
    """
    OFFICIAL = "OFFICIAL"

    """
    https://en.wikipedia.org/wiki/Belarusian_Latin_alphabet
    """
    LATIN = "LATIN"

    """
    Łacinka with all diactric removed.
    Useful for cases where only standard lacin letters are 
    accepted such as URLs.
    """
    LATIN_NO_DIACTRIC = "LATIN_NO_DIACTRIC"
