from belorthography.cases import Case
from belorthography.converters import translit_lat_to_lat_no_diactric, translit_cyr_taras_to_lat, translit_cyr_nar_to_cyr_taras

def convert(text, source_case, target_case):
    """
    Convert function select implementation based on source and target cases.
    """
    if target_case == Case.LAT:
        if source_case == Case.CYR_NAR or source_case == Case.CYR_TARAS:
            return translit_cyr_taras_to_lat.convert(text)

    if target_case == Case.LAT_NO_DIACTRIC:
        if source_case == Case.CYR_NAR or source_case == Case.CYR_TARAS:
            latin = convert(text, source_case, Case.LAT)
            return convert(latin, Case.LAT, Case.LAT_NO_DIACTRIC)
        elif source_case == Case.LAT:
            return translit_lat_to_lat_no_diactric.convert(text)

    if target_case == Case.CYR_TARAS:
        if source_case == Case.CYR_NAR:
            return translit_cyr_nar_to_cyr_taras.convert(text)

    raise ValueError(f'Conversion from {source_case} to {target_case} is not supported.')
