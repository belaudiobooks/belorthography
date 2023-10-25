'''Converts Narkamauka to Taraskievica.

Rules and examples are taken from here: https://knihi.com/storage/pravapis2005.html
'''

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
    return is_consonant(l) and l != 'г' and l != 'к' and l != 'х'

def is_soft_consonant(t, i):
    # if current symbol is space - move to the next letter as it affects
    # softening as if space was not present.
    if t[i] == ' ':
        if len(t) == i + 1:
            return False
        return is_softening_vowel(t[i + 1]) or is_soft_consonant(t, i + 1)
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

def convert(text):
    # Add extra space at the end to avoid checking for out of bounds.
    ot = text + ' '
    # We operate on lowercase text to avoid checking for uppercase letters.
    # But when adding letters to the final result list we'll be using the
    # original text.
    t = text.lower() + ' '
    result = []
    i = 0
    while i < len(t):
        l = t[i]
        # https://knihi.com/storage/pravapis2005.html#texth2_8
        if (l == 'с' or l == 'з' or l == 'ц') and is_soft_consonant(t, i + 1):
            result.append(ot[i])
            result.append('ь')
        # https://knihi.com/storage/pravapis2005.html#texth2_8
        elif l == 'д' and t[i + 1] == 'з' and is_soft_consonant(t, i + 2):
            result.append(ot[i])
            result.append(ot[i + 1])
            result.append('ь')
            i += 1
        elif (l == 'н' or l == 'л') and t[i + 1] == l and is_soft_consonant(t, i + 1):
            result.append(ot[i])
            result.append('ь')
        # https://knihi.com/storage/pravapis2005.html#texth2_16
        elif (l == 'з' or l == 'с' or l == 'л' or l == 'н') and (t[i + 1] == "'" or t[i + 1] == '’'):
            if is_softening_vowel(t[i + 2]):
                result.append(ot[i])
                result.append('ь')
                i += 1
        else:
            result.append(ot[i])

        # TODO: implement і => й like here: https://knihi.com/storage/pravapis2005.html#texth2_4
        # TODO: keep case of inserted letters. For example НАСЕННЕ => НАСЕНЬНЕ.
        i += 1
    # Don't forget to remove the extra space we added at the beginning.
    return ''.join(result[:-1])