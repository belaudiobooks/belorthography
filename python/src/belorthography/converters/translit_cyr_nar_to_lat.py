from belorthography.converters import translit_cyr_taras_to_lat

def convert(text):
    # TODO: rework this to implement translation to Taraskievica first
    # and then to lacinka.
    return translit_cyr_taras_to_lat.convert(text)