from belorthography.orthographies import Orthography
from belorthography.converters import (
    translit_lat_to_lat_no_diactric,
    translit_cyr_taras_to_lat,
    translit_cyr_nar_to_cyr_taras,
)


def convert(text, source_case, target_case):
    """
    Convert function select implementation based on source and target cases.
    """
    if target_case == Orthography.LATIN:
        if source_case == Orthography.OFFICIAL:
            taras = convert(text, Orthography.OFFICIAL, Orthography.CLASSICAL)
            return convert(taras, Orthography.CLASSICAL, Orthography.LATIN)
        if source_case == Orthography.CLASSICAL:
            return translit_cyr_taras_to_lat.convert(text)

    if target_case == Orthography.LATIN_NO_DIACTRIC:
        if source_case == Orthography.OFFICIAL or source_case == Orthography.CLASSICAL:
            latin = convert(text, source_case, Orthography.LATIN)
            return convert(latin, Orthography.LATIN, Orthography.LATIN_NO_DIACTRIC)
        elif source_case == Orthography.LATIN:
            return translit_lat_to_lat_no_diactric.convert(text)

    if target_case == Orthography.CLASSICAL:
        if source_case == Orthography.OFFICIAL:
            return translit_cyr_nar_to_cyr_taras.convert(text)

    raise ValueError(
        f"Conversion from {source_case} to {target_case} is not supported."
    )
