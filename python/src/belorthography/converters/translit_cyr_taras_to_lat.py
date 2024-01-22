from belorthography.converters.util import (
    is_apostrophe,
    is_softening_vowel,
    is_vowel,
    is_cyrillic,
)

# Common variable names in functions. Shortened to save space.
# l - letter
# t - text
# i - index

MAPPING = (
    ("дзь", "dź"),
    ("дз", "dz"),
    ("дж", "dž"),
    ("ль", "l"),
    ("нь", "ń"),
    ("ць", "ć"),
    ("сь", "ś"),
    ("зь", "ź"),
    ("а", "a"),
    ("б", "b"),
    ("ц", "c"),
    ("ч", "č"),
    ("д", "d"),
    ("з", "z"),
    ("з", "z"),
    ("э", "e"),
    ("ф", "f"),
    ("г", "h"),
    ("х", "ch"),
    ("і", "i"),
    ("и", "i"),
    ("й", "j"),
    ("к", "k"),
    ("л", "ł"),
    ("м", "m"),
    ("н", "n"),
    ("о", "o"),
    ("п", "p"),
    ("р", "r"),
    ("с", "s"),
    ("ш", "š"),
    ("т", "t"),
    ("у", "u"),
    ("ў", "ŭ"),
    ("в", "v"),
    ("ы", "y"),
    ("з", "z"),
    ("ж", "ž"),
)


def build_suffix_tree(mappings):
    """Build a suffix tree to quickly find the mapping for a given text rather than doing O(n) search
    for each letter."""
    tree = {}
    for cyr, lat in mappings:
        node = tree
        for l in cyr:  # noqa
            if l not in node:
                node[l] = {}
            node = node[l]
        node[""] = lat
    tree[""] = None
    return tree


# Suffix tree is used to quickly find the mapping for a given text rather than doing O(n) search.
# Tree has form like:
# {
#   'д': {
#     'з': {
#       'ь': {'': 'dź'}
#       '': {'': 'dz'}
#     },
#     'ж': {'': 'dž'}
#   },
#   ...
# }
TREE = build_suffix_tree(MAPPING)

SOFTEN_VOWEL_MAPPING = {
    "е": "e",
    "ё": "o",
    "ю": "u",
    "я": "a",
}


def can_be_softened(l):  # noqa
    return l == "л" or l == "н" or l == "ц" or l == "с" or l == "з"


def matches(t, i, str):
    """Whether the text at the specified index matches the specified string."""
    return t[i : i + len(str)] == str


def find_mapping(t, i):
    """Find the mapping for the specified text at the specified index."""
    if not t[i] in TREE:
        return None
    node = TREE
    cyr = ""
    while t[i] in node:
        cyr += t[i]
        node = node[t[i]]
        i += 1
    return cyr, node[""]


def keep_same_case(t, i, new):
    assert new.islower()
    # If the first letter is lower - assume the whole text lower case. We don't support
    # odd cases like aBcD.
    if t[i].islower():
        return new

    # If the first two letters are uppper - assume whole text is upper case.
    # Also if this is the last letter and previous letters upper - assume whole text is
    # upper case.
    if t[i].isupper() and (
        t[i + 1].isupper()
        or t[i - 1].isupper()
        or (is_apostrophe(t[i - 1]) and t[i - 2].isupper())
    ):
        return new.upper()

    # First letter is upper and the second one is lower. Assume this is capitalized word.
    return new.capitalize()


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
        return result.append(keep_same_case(ot, i, l))

    while i < len(t):
        l = t[i]  # noqa
        p = t[i - 1]
        if is_apostrophe(l) or l == "ь":
            i += 1
            continue

        if l != "і" and is_softening_vowel(l):
            acc = ""
            if p == "л":
                acc = ""
            elif is_vowel(p) or p == "ў" or p == "ь" or not is_cyrillic(p):
                acc = "j"
            else:
                acc = "i"
            acc += SOFTEN_VOWEL_MAPPING[l]
            append_letter(acc, i)
            i += 1
            continue

        if l == "і":
            if p == "ь" or is_apostrophe(p):
                append_letter("ji", i)
                i += 1
                continue

        if l == "л" and is_softening_vowel(t[i + 1]):
            append_letter("l", i)
            i += 1
            continue

        mapping = find_mapping(t, i)
        if mapping is None:
            result.append(ot[i])
            i += 1
            continue
        else:
            cyr, lat = mapping
            append_letter(lat, i)
            i += len(cyr)
    # Don't forget to remove the extra space we added at the beginning.
    return "".join(result[:-1])
