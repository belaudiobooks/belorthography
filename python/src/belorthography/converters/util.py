"""
Utility functions for working with belarusian letters.
"""
# Common variable names in functions. Shortened to save space.
# l - letter
# t - text
# i - index

def is_cyrillic(l):
    return ord(l) >= ord('а') and ord(l) <= ord ('я') or l == 'і' or l == 'ў' or l == 'ё'

def is_vowel(l):
    return l == 'а' or l == 'о' or l == 'у' or l == 'ы' or l == 'э' or l == 'е' or l == 'ё' or l == 'і' or l == 'ю' or l == 'я'

def is_softening_vowel(l):
    '''Whether the vowel softens the previous consonant.'''
    return l == 'і' or l == 'ю' or l == 'я' or l == 'е' or l == 'ё'

def is_consonant(l):
    return is_cyrillic(l) and not is_vowel(l) and not l == 'ь'

def is_softening_consonant(l):
    '''Consontant that softens the previous consonant if it itself is soft.'''
    return is_consonant(l) and l != 'г' and l != 'к' and l != 'х' and l != 'т'

def is_soft_consonant(t, i):
    # We are interested only when the current letter can soften the previous one.
    # Not all consonants soften previous ones. For example soft 'к' doesn't.
    if not is_softening_consonant(t[i]):
        return False
    if t[i + 1] == 'ь':
        return True
    # If current consonant followed by a softening vowel - it softens.
    if is_softening_vowel(t[i + 1]):
        return True
    # If current consonant is followed by another soft consonant - it softens.
    return is_soft_consonant(t, i + 1)

def is_apostrophe(l):
    return l == "'" or l == "ʼ" or l == "’"
