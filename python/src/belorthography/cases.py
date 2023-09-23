"""
Class mimic to enum to keep consistent definition
all possible transliteration case options.
"""


class Case:
    """
    LAT - Represent case: Łacinka.
    TODO: Add description and references.
    """
    LAT = "LAT"

    """
    Łacinka with all diactric removed.
    Useful for cases where only standard lacin letters are 
    accepted such as URLs.
    """
    LAT_NO_DIACTRIC = "LAT_NO_DIACTRIC"

    """
    CYR - Represent case: Kirylica.
    TODO: Add description and references.
    """
    CYR_TARAS = "CYR_TARAS"

    """
    CYR_NARCOM - Represent case: Kirylica narkomaŭka.
    TODO: Add description and references.
    """
    CYR_NAR = "CYR_NAR"
