'''Converts Narkamauka to Taraskievica.

Rules and examples are taken from here: https://knihi.com/storage/pravapis2005.html
'''


from belorthography.converters.util import is_soft_consonant, is_softening_vowel

# Common variable names in functions. Shortened to save space.
# l - letter
# t - text
# i - index

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