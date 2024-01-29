"""Converts Narkamauka to Taraskievica.

Rules and examples are taken from here: https://knihi.com/storage/pravapis2005.html
"""

from belorthography.converters.util import (
    is_apostrophe,
    is_cyrillic,
    is_soft_consonant,
    is_softening_vowel,
)

# Common variable names in functions. Shortened to save space.
# l - letter
# t - text
# i - index

# https://knihi.com/storage/pravapis2005.html#texth2_8
PREPOSITIONS = ["з", "без", "бяз", "праз", "цераз"]


# Only soften last letter of a preposition, but not any other word.
# See https://www.facebook.com/groups/pramovu/posts/3554247581516231/
def is_preposition_followed_by_soft(t, i):
    # check if 'i' points at the last letter in a word. If not - this is not a preposition.
    # or if we reached the end of the text
    if t[i + 1] != " " or len(t) == i + 2:
        return False
    if not is_soft_consonant(t, i + 2) and not is_softening_vowel(t[i + 2]):
        return False
    for p in PREPOSITIONS:
        # 1. the character before the preposition should not be a letter.
        # 2. substring starting len(p) letters before should match.
        if not is_cyrillic(t[i - len(p)]) and t[i - len(p) + 1 : i + 1] == p:
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
    ot = text + " "
    # We operate on lowercase text to avoid checking for uppercase letters.
    # But when adding letters to the final result list we'll be using the
    # original text.
    t = text.lower() + " "
    result = []
    i = 0

    def append_letter(l, i):  # noqa
        return result.append(maybe_upper_case(ot, i, l))

    while i < len(t):
        l = t[i]  # noqa
        # https://knihi.com/storage/pravapis2005.html#texth2_8
        if (l == "с" or l == "з" or l == "ц") and is_soft_consonant(t, i + 1):
            result.append(ot[i])
            append_letter("ь", i)
        # https://knihi.com/storage/pravapis2005.html#texth2_8
        elif l == "з" and is_preposition_followed_by_soft(t, i):
            result.append(ot[i])
            append_letter("ь", i)
        # https://knihi.com/storage/pravapis2005.html#texth2_8
        elif l == "д" and t[i + 1] == "з" and is_soft_consonant(t, i + 2):
            result.append(ot[i])
            result.append(ot[i + 1])
            append_letter("ь", i + 1)
            i += 1
        elif (l == "н" or l == "л") and t[i + 1] == l and is_soft_consonant(t, i + 1):
            result.append(ot[i])
            append_letter("ь", i)
        # https://knihi.com/storage/pravapis2005.html#texth2_16
        elif (l == "з" or l == "с" or l == "л" or l == "н") and is_apostrophe(t[i + 1]):
            if is_softening_vowel(t[i + 2]):
                result.append(ot[i])
                append_letter("ь", i)
                i += 1
        else:
            result.append(ot[i])

        i += 1

    # Don't forget to remove the extra space we added at the beginning.
    return "".join(result[:-1])
