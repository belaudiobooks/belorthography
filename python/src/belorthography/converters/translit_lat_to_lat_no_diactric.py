'''
Converts Latin case to no diactric variant.
'''

REPLACEMENTS = {
    'Ć': 'C',
    'ć': 'c',
    'Č': 'C',
    'č': 'c',
    'Ł': 'L',
    'ł': 'l',
    'Ś': 'S',
    'ś': 's',
    'Š': 'S',
    'š': 's',
    'Ŭ': 'U',
    'ŭ': 'u',
    'Ź': 'Z',
    'ź': 'z',
    'Ž': 'Z',
    'ž': 'z',
    'Ń': 'N',
    'ń': 'n',
}

def convert(text):
    result = []
    for char in text:
        result.append(REPLACEMENTS.get(char, char))
    return ''.join(result)
