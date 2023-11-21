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

# https://knihi.com/storage/pravapis2005.html#texth2_8
PREPOSITIONS = ['з', 'без', 'бяз', 'праз', 'цераз']

def is_preposition_followed_by_soft(t, i):
    # check if 'i' points at the last letter in a word. If not - this is not a preposition.
    # or if we reached the end of the text
    if t[i + 1] != ' ' or len(t) == i + 2:
        return False
    if not is_soft_consonant(t, i + 2) and not is_softening_vowel(t[i + 2]):
        return False
    for p in PREPOSITIONS:
        # 1. the character before the preposition should not be a letter.
        # 2. substring starting len(p) letters before should match.
        if not is_cyrillic(t[i - len(p)]) and  t[i - len(p) + 1:i + 1] == p:
            return True
    return False

def maybe_upper_case(original_text: str, i, new_text):
    # if the current character lower case - newly inserted text
    # should be lower case as well.
    if original_text[i].islower():
        return new_text
    next_char = original_text[i + 1]

    # if current char is upper and the next char is upper - assume that the whole word
    # is upper case. Newily inserted text should be upper case as well.
    if next_char.isupper():
        return new_text.upper()

    # Current character is upper case but the next one is lower. New text should be
    # lower case as well.
    return new_text

def convert(text):
    # Add extra space at the end to avoid checking for out of bounds.
    ot = text + ' '
    # We operate on lowercase text to avoid checking for uppercase letters.
    # But when adding letters to the final result list we'll be using the
    # original text.
    t = text.lower() + ' '
    result = []
    i = 0
    append_letter = lambda l, i: result.append(maybe_upper_case(ot, i, l))
    while i < len(t):
        l = t[i]
        # https://knihi.com/storage/pravapis2005.html#texth2_8
        if (l == 'с' or l == 'з' or l == 'ц') and is_soft_consonant(t, i + 1):
            result.append(ot[i])
            append_letter('ь', i)
        # https://knihi.com/storage/pravapis2005.html#texth2_8
        elif l == 'з' and is_preposition_followed_by_soft(t, i):
            result.append(ot[i])
            append_letter('ь', i)
        # https://knihi.com/storage/pravapis2005.html#texth2_8
        elif l == 'д' and t[i + 1] == 'з' and is_soft_consonant(t, i + 2):
            result.append(ot[i])
            result.append(ot[i + 1])
            append_letter('ь', i + 1)
            i += 1
        elif (l == 'н' or l == 'л') and t[i + 1] == l and is_soft_consonant(t, i + 1):
            result.append(ot[i])
            append_letter('ь', i)
        # https://knihi.com/storage/pravapis2005.html#texth2_16
        elif (l == 'з' or l == 'с' or l == 'л' or l == 'н') and (t[i + 1] == "'" or t[i + 1] == '’'):
            if is_softening_vowel(t[i + 2]):
                result.append(ot[i])
                append_letter('ь', i)
                i += 1
        else:
            result.append(ot[i])

        i += 1

    # Don't forget to remove the extra space we added at the beginning.
    return ''.join(result[:-1])