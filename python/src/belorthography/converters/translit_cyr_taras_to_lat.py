import re

from belorthography.converters.util import is_softening_vowel, is_vowel, is_cyrillic

# Common variable names in functions. Shortened to save space.
# l - letter
# t - text
# i - index

MAPPING = (
    ('дзь', 'dź'),
    ('дж', 'dž'),
    ('ль', 'l'),
    ('нь', 'ń'),
    ('ць', 'ć'),
    ('сь', 'ś'),
    ('зь', 'ź'),
    ('а', 'a'),
    ('б', 'b'),
    ('ц', 'c'),
    ('ч', 'č'),
    ('д', 'd'),
    ('з', 'z'),
    ('з', 'z'),
    ('э', 'e'),
    ('ф', 'f'),
    ('г', 'h'),
    ('х', 'ch'),
    ('і', 'i'),
    ('й', 'j'),
    ('к', 'k'),
    ('л', 'ł'),
    ('м', 'm'),
    ('н', 'n'),
    ('о', 'o'),
    ('п', 'p'),
    ('р', 'r'),
    ('с', 's'),
    ('ш', 'š'),
    ('т', 't'),
    ('у', 'u'),
    ('ў', 'ŭ'),
    ('в', 'v'),
    ('ы', 'y'),
    ('з', 'z'),
    ('ж', 'ž'),
)

SOFTEN_VOWEL_MAPPING = {
    'е': 'e',
    'ё': 'o',
    'ю': 'u',
    'я': 'a',
}

def can_be_softened(l):
    return l == 'л' or l == 'н' or l == 'ц' or l == 'с' or l == 'з'

def matches(t, i, str):
    '''Whether the text at the specified index matches the specified string.'''
    return t[i:i + len(str)] == str

def find_mapping(t, i):
    '''Find the mapping for the specified text at the specified index.'''
    for cyr, lat in MAPPING:
        if matches(t, i, cyr):
            return cyr, lat
    return None

def keep_same_case(original, i, new):
    assert new.islower()
    # If the first letter is lower - assume the whole text lower case. We don't support
    # odd cases like aBcD.
    if original[i].islower():
        return new

    # If the first two letters are uppper - assume whole text is upper case.
    if original[i].isupper() and original[i+1].isupper():
        return new.upper()

    # First letter is upper and the second one is lower. Assume this is capitalized word.
    return new.capitalize()

def convert(text):# Add extra space at the end to avoid checking for out of bounds.
    ot = text + ' '
    # We operate on lowercase text to avoid checking for uppercase letters.
    # But when adding letters to the final result list we'll be using the
    # original text.
    t = text.lower() + ' '
    result = []
    i = 0
    append_letter = lambda l, i: result.append(keep_same_case(ot, i, l))
    while i < len(t):
        l = t[i]
        p = t[i - 1]
        if l == "'" or l == "ʼ":
            i += 1
            continue

        if l != 'і' and is_softening_vowel(l):
            acc = ''
            if p == 'л':
                acc = ''
            elif is_vowel(p) or p == 'ў' or p == 'ь' or not is_cyrillic(p):
                acc = 'j'
            else:
                acc = 'i'
            acc += SOFTEN_VOWEL_MAPPING[l]
            append_letter(acc, i)
            i += 1
            continue

        if l == 'і':
            if p == 'ь':
                append_letter('ji', i)
                i += 1
                continue

        if l == 'л' and is_softening_vowel(t[i + 1]):
            append_letter('l', i)
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
    return ''.join(result[:-1])

# TODO:
# Original version of the script was taken from the resource: https://nashaniva.com/
# Source: view-source:https://nashaniva.com/?c=latn
# Since the script is optimized for Nasha Niva's requirements,
# there are some places that will be reworked to make the converter more generic.

def convert2(text):
    conv = ' ' + text + ' '
    conv = re.sub(
        # Match any single character that is not one of the listed Cyrillic letters.
        r'([^абвгдеёжзийклмнопрстуфхцчшщъыьэюяіў])' +
        # Match one of the specified words: цераз, праз, без, or з.
        r'(цераз|праз|без|з)' +
        # Match one or more characters that are not the listed Cyrillic letters or a hyphen.
        r'([^абвгдеёжзийклмнопрстуфхцчшщъыьэюяіў\-]+)' +
        # Match one of the specified endings: я, е, ё, ю, і or a combination of certain consonants and the endings.
        r'([яеёюі]|[бвлзнмпсцф]+[яеёюіь]|дз[бвлзнмпсцф]?[яеёюіь])',
        # \1: Refers to the first captured group, which matches any single character that is not one of the listed Cyrillic letters.
        # \2: Refers to the second captured group, which matches one of the specified words: цераз, праз, без, or з.
        # ь: Inserts the character 'ь' after the second captured group.
        # \3: Refers to the third captured group, which matches one or more characters that are not the listed Cyrillic letters or a hyphen.
        # \4: Refers to the fourth captured group, which matches one of the specified endings: я, е, ё, ю, і or a combination of certain consonants and the endings.
        r'\1\2ь\3\4',
        conv,
        # re.I flag is used to make the matching case-insensitive
        flags=re.I)

    conv = re.sub(
        # Capture group 1: Match a non-word character (anything other than letters, digits, or underscores).
        r'(\W)' +
        # Capture group 2: Match two or more uppercase Cyrillic letters.
        r'([АБВГДЕЁЖЗІИЙКЛМНОПРСТУЎФХЦЧШЩЪЫЬЭЮЯ]{2,})',
        # x.group(1): Refers to the content of the first captured group, which is the non-word character.
        # ' ': Inserts four spaces (adjust the number of spaces as desired).
        # x.group(2).lower(): Refers to the content of the second captured group (the uppercase Cyrillic word), and .lower() converts it to lowercase.
        # ' ': Inserts four spaces again.
                  lambda x: x.group(1) + '    ' + x.group(2).lower() + '    ',
        conv)
    conv = conv.replace('’', "'")

    # Don't have examples for the following rules.
    # conv = conv.replace('сллі', 'ślli')
    # conv = conv.replace('ссмі', 'śśmi')
    # conv = conv.replace('ссні', 'śśni')
    # conv = conv.replace('сцці', 'śćci')
    # conv = conv.replace('ззві', 'źźvi')
    # conv = conv.replace('цвлі', 'ćvli')

    conv = conv.replace('ллі', 'lli')
    conv = conv.replace('ссі', 'śsi')

    # Don't have examples for the following rules.
    # conv = conv.replace('слле', 'ślle')
    # conv = conv.replace('ссме', 'śśmie')
    # conv = conv.replace('ссне', 'śśnie')
    # conv = conv.replace('сцце', 'śćcie')
    # conv = conv.replace('ззве', 'źźvie')
    # conv = conv.replace('цвле', 'ćvle')

    conv = conv.replace('лле', 'lle')

    # Don't have examples for the following rules.
    # conv = conv.replace('ссе', 'śsie')
    # conv = conv.replace('сллё', 'śllo')
    # conv = conv.replace('ссмё', 'śśmio')
    # conv = conv.replace('сснё', 'śśnio')
    # conv = conv.replace('сццё', 'śćcio')
    # conv = conv.replace('ззвё', 'źźvio')
    # conv = conv.replace('цвлё', 'ćvlo')
    # conv = conv.replace('ллё', 'llo')
    # conv = conv.replace('ссё', 'śsio')
    # conv = conv.replace('сллю', 'śllu')
    # conv = conv.replace('ссмю', 'śśmiu')
    # conv = conv.replace('ссню', 'śśniu')
    # conv = conv.replace('сццю', 'śćciu')
    # conv = conv.replace('ззвю', 'źźviu')
    # conv = conv.replace('цвлю', 'ćvlu')
    # conv = conv.replace('ллю', 'llu')
    # conv = conv.replace('ссю', 'śsiu')
    # conv = conv.replace('слля', 'ślla')
    # conv = conv.replace('ссмя', 'śśmia')
    # conv = conv.replace('ссня', 'śśnia')
    # conv = conv.replace('сцця', 'śćcia')
    # conv = conv.replace('ззвя', 'źźvia')
    # conv = conv.replace('цвля', 'ćvla')
    conv = conv.replace('лля', 'lla')
    conv = conv.replace('сся', 'śsia')


    # ------------- tested -------------

    conv = conv.replace('Спець', 'Śpieć')
    conv = conv.replace('Спец', 'Śpiec')
    conv = conv.replace('спець', 'śpieć')
    conv = conv.replace('спец', 'śpiec')
    conv = conv.replace('Сцве', 'Śćvie')
    conv = conv.replace('Сцвё', 'Śćvio')
    conv = conv.replace('Сцвю', 'Śćviu')
    conv = conv.replace('Сцвя', 'Śćvia')
    conv = conv.replace('Сцві', 'Śćvi')
    conv = conv.replace('сцве', 'śćvie')
    conv = conv.replace('сцвё', 'śćvio')
    conv = conv.replace('сцвю', 'śćviu')
    conv = conv.replace('сцвя', 'śćvia')
    conv = conv.replace('сцві', 'śćvi')

    conv = conv.replace('Цве', 'Ćvie')
    conv = conv.replace('Цвё', 'Ćvio')
    conv = conv.replace('Цвю', 'Ćviu')
    conv = conv.replace('Цвя', 'Ćvia')
    conv = conv.replace('Цві', 'Ćvi')
    conv = conv.replace('цве', 'ćvie')
    conv = conv.replace('цвё', 'ćvio')
    conv = conv.replace('цвю', 'ćviu')
    conv = conv.replace('цвя', 'ćvia')
    conv = conv.replace('цві', 'ćvi')

    conv = conv.replace('Посте', 'Postje')
    conv = conv.replace('Постё', 'Postjo')
    conv = conv.replace('Постю', 'Postju')
    conv = conv.replace('Постя', 'Postja')
    conv = conv.replace('посте', 'postje')
    conv = conv.replace('постё', 'postjo')
    conv = conv.replace('постю', 'postju')
    conv = conv.replace('постя', 'postja')

    conv = conv.replace('Шмате', 'Šmatje')
    conv = conv.replace('Шматё', 'Šmatjo')
    conv = conv.replace('Шматю', 'Šmatju')
    conv = conv.replace('Шматя', 'Šmatja')
    conv = conv.replace('шмате', 'šmatje')
    conv = conv.replace('шматё', 'šmatjo')
    conv = conv.replace('шматю', 'šmatju')
    conv = conv.replace('шматя', 'šmatja')

    conv = conv.replace('Дзете', 'Dzetje')
    conv = conv.replace('Дзетё', 'Dzetjo')
    conv = conv.replace('Дзетю', 'Dzetju')
    conv = conv.replace('Дзетя', 'Dzetja')
    conv = conv.replace('дзете', 'dzetje')
    conv = conv.replace('дзетё', 'dzetjo')
    conv = conv.replace('дзетю', 'dzetju')
    conv = conv.replace('дзетя', 'dzetja')

    conv = conv.replace('ыяе', 'yjaje')
    conv = conv.replace('ыяё', 'yjajo')
    conv = conv.replace('ыяю', 'yjaju')
    conv = conv.replace('іяе', 'іjaje')
    conv = conv.replace('іяю', 'іjaju')
    conv = conv.replace('эяю', 'ejaju')
    conv = conv.replace('іёю', 'іjoju')
    conv = conv.replace('яёю', 'яjoju')
    conv = conv.replace('аёю', 'ajoju')
    conv = conv.replace('уяю', 'ujaju')
    conv = conv.replace('ыёю', 'yjoju')
    conv = conv.replace('аюю', 'ajuju')
    conv = conv.replace('іюю', 'іjuju')
    conv = conv.replace('аяю', 'ajaju')
    conv = conv.replace('уюю', 'ujuju')
    conv = conv.replace('ыюю', 'yjuju')
    conv = conv.replace('ояю', 'ojaju')
    conv = conv.replace('іяё', 'іjajo')
    conv = conv.replace('уёю', 'ujoju')

    conv = conv.replace('Збі', 'Źbi')
    conv = conv.replace('Зві', 'Źvi')
    conv = conv.replace('Ззі', 'Źzi')
    conv = conv.replace('Злі', 'Źlі')
    conv = conv.replace('Змі', 'Źmi')
    conv = conv.replace('Зні', 'Źni')
    conv = conv.replace('Зці', 'Źci')
    conv = conv.replace('Здзі', 'Ździ')
    conv = conv.replace('Збе', 'Źbie')
    conv = conv.replace('Зве', 'Źvie')
    conv = conv.replace('Ззе', 'Źzie')
    conv = conv.replace('Зле', 'Źle')
    conv = conv.replace('Зме', 'Źmie')
    conv = conv.replace('Зне', 'Źnie')
    conv = conv.replace('Зце', 'Źcie')
    conv = conv.replace('Здзе', 'Ździe')
    conv = conv.replace('Збё', 'Źbio')
    conv = conv.replace('Звё', 'Źvio')
    conv = conv.replace('Ззё', 'Źzio')
    conv = conv.replace('Злё', 'Źlo')
    conv = conv.replace('Змё', 'Źmio')
    conv = conv.replace('Знё', 'Źnio')
    conv = conv.replace('Зцё', 'Źcio')
    conv = conv.replace('Здзё', 'Ździo')
    conv = conv.replace('Збю', 'Źbiu')
    conv = conv.replace('Звю', 'Źviu')
    conv = conv.replace('Ззю', 'Źziu')
    conv = conv.replace('Злю', 'Źlu')
    conv = conv.replace('Змю', 'Źmiu')
    conv = conv.replace('Зню', 'Źniu')
    conv = conv.replace('Зцю', 'Źciu')
    conv = conv.replace('Здзю', 'Ździu')
    conv = conv.replace('Збя', 'Źbia')
    conv = conv.replace('Звя', 'Źvia')
    conv = conv.replace('Ззя', 'Źzia')
    conv = conv.replace('Зля', 'Źla')
    conv = conv.replace('Змя', 'Źmia')
    conv = conv.replace('Зня', 'Źnia')
    conv = conv.replace('Зця', 'Źcia')
    conv = conv.replace('Здзя', 'Ździa')
    conv = conv.replace('збі', 'źbi')
    conv = conv.replace('зві', 'źvi')
    conv = conv.replace('ззі', 'źzi')
    conv = conv.replace('злі', 'źlі')
    conv = conv.replace('змі', 'źmi')
    conv = conv.replace('зні', 'źni')
    conv = conv.replace('зці', 'źci')
    conv = conv.replace('здзі', 'ździ')
    conv = conv.replace('збе', 'źbie')
    conv = conv.replace('зве', 'źvie')
    conv = conv.replace('ззе', 'źzie')
    conv = conv.replace('зле', 'źle')
    conv = conv.replace('зме', 'źmie')
    conv = conv.replace('зне', 'źnie')
    conv = conv.replace('зце', 'źcie')
    conv = conv.replace('здзе', 'ździe')
    conv = conv.replace('збё', 'źbio')
    conv = conv.replace('звё', 'źvio')
    conv = conv.replace('ззё', 'źzio')
    conv = conv.replace('злё', 'źlo')
    conv = conv.replace('змё', 'źmio')
    conv = conv.replace('знё', 'źnio')
    conv = conv.replace('зцё', 'źcio')
    conv = conv.replace('здзё', 'ździo')
    conv = conv.replace('збю', 'źbiu')
    conv = conv.replace('звю', 'źviu')
    conv = conv.replace('ззю', 'źziu')
    conv = conv.replace('злю', 'źlu')
    conv = conv.replace('змю', 'źmiu')
    conv = conv.replace('зню', 'źniu')
    conv = conv.replace('зцю', 'źciu')
    conv = conv.replace('здзю', 'ździu')
    conv = conv.replace('збя', 'źbia')
    conv = conv.replace('звя', 'źvia')
    conv = conv.replace('ззя', 'źzia')
    conv = conv.replace('зля', 'źla')
    conv = conv.replace('змя', 'źmia')
    conv = conv.replace('зня', 'źnia')
    conv = conv.replace('зця', 'źcia')
    conv = conv.replace('здзя', 'ździa')

    conv = conv.replace('Сфі', 'Śfi')
    conv = conv.replace('Сбі', 'Śbi')
    conv = conv.replace('Сві', 'Śvi')
    conv = conv.replace('Слі', 'Śli')
    conv = conv.replace('Смі', 'Śmi')
    conv = conv.replace('Сні', 'Śni')
    conv = conv.replace('Спі', 'Śpi')
    conv = conv.replace('Сці', 'Ści')
    conv = conv.replace('Сфе', 'Śfie')
    conv = conv.replace('Сбе', 'Śbie')
    conv = conv.replace('Све', 'Śvie')
    conv = conv.replace('Сле', 'Śle')
    conv = conv.replace('Сме', 'Śmie')
    conv = conv.replace('Сне', 'Śnie')
    conv = conv.replace('Спе', 'Śpie')
    conv = conv.replace('Сце', 'Ście')
    conv = conv.replace('Сфё', 'Śfio')
    conv = conv.replace('Сбё', 'Śbio')
    conv = conv.replace('Свё', 'Śvio')
    conv = conv.replace('Слё', 'Ślo')
    conv = conv.replace('Смё', 'Śmio')
    conv = conv.replace('Снё', 'Śnio')
    conv = conv.replace('Спё', 'Śpio')
    conv = conv.replace('Сцё', 'Ścio')
    conv = conv.replace('Сфю', 'Śfiu')
    conv = conv.replace('Сбю', 'Śbiu')
    conv = conv.replace('Свю', 'Śviu')
    conv = conv.replace('Слю', 'Ślu')
    conv = conv.replace('Смю', 'Śmiu')
    conv = conv.replace('Сню', 'Śniu')
    conv = conv.replace('Спю', 'Śpiu')
    conv = conv.replace('Сцю', 'Ściu')
    conv = conv.replace('Сфя', 'Śfia')
    conv = conv.replace('Сбя', 'Śbia')
    conv = conv.replace('Свя', 'Śvia')
    conv = conv.replace('Сля', 'Śla')
    conv = conv.replace('Смя', 'Śmia')
    conv = conv.replace('Сня', 'Śnia')
    conv = conv.replace('Спя', 'Śpia')
    conv = conv.replace('Сця', 'Ścia')
    conv = conv.replace('Cць', 'Ść')
    conv = conv.replace('сфі', 'śfi')
    conv = conv.replace('сбі', 'śbi')
    conv = conv.replace('сві', 'śvi')
    conv = conv.replace('слі', 'śli')
    conv = conv.replace('смі', 'śmi')
    conv = conv.replace('сні', 'śni')
    conv = conv.replace('спі', 'śpi')
    conv = conv.replace('сці', 'ści')
    conv = conv.replace('сфе', 'śfie')
    conv = conv.replace('сбе', 'śbie')
    conv = conv.replace('све', 'śvie')
    conv = conv.replace('сле', 'śle')
    conv = conv.replace('сме', 'śmie')
    conv = conv.replace('сне', 'śnie')
    conv = conv.replace('спе', 'śpie')
    conv = conv.replace('сце', 'ście')
    conv = conv.replace('сфё', 'śfio')
    conv = conv.replace('сбё', 'śbio')
    conv = conv.replace('свё', 'śvio')
    conv = conv.replace('слё', 'ślo')
    conv = conv.replace('смё', 'śmio')
    conv = conv.replace('снё', 'śnio')
    conv = conv.replace('спё', 'śpio')
    conv = conv.replace('сцё', 'ścio')
    conv = conv.replace('сфю', 'śfiu')
    conv = conv.replace('сбю', 'śbiu')
    conv = conv.replace('свю', 'śviu')
    conv = conv.replace('слю', 'ślu')
    conv = conv.replace('смю', 'śmiu')
    conv = conv.replace('сню', 'śniu')
    conv = conv.replace('спю', 'śpiu')
    conv = conv.replace('сцю', 'ściu')
    conv = conv.replace('сфя', 'śfia')
    conv = conv.replace('сбя', 'śbia')
    conv = conv.replace('свя', 'śvia')
    conv = conv.replace('сля', 'śla')
    conv = conv.replace('смя', 'śmia')
    conv = conv.replace('сня', 'śnia')
    conv = conv.replace('спя', 'śpia')
    conv = conv.replace('сця', 'ścia')
    conv = conv.replace('сць', 'ść')

    conv = conv.replace('нья', 'ńja')
    conv = conv.replace('ньё', 'ńjo')
    conv = conv.replace('нье', 'ńje')
    conv = conv.replace('нью', 'ńju')
    conv = conv.replace('ньи', 'ńji')
    conv = conv.replace('Нья', 'Ńja')
    conv = conv.replace('Ньё', 'Ńjo')
    conv = conv.replace('Нье', 'Ńje')
    conv = conv.replace('Нью', 'Ńju')
    conv = conv.replace('Ньи', 'Ńji')

    conv = conv.replace('сья', 'śja')
    conv = conv.replace('сьё', 'śjo')
    conv = conv.replace('сье', 'śje')
    conv = conv.replace('сью', 'śju')
    conv = conv.replace('сьи', 'śji')
    conv = conv.replace('Сья', 'Śja')
    conv = conv.replace('Сьё', 'Śjo')
    conv = conv.replace('Сье', 'Śje')
    conv = conv.replace('Сью', 'Śju')
    conv = conv.replace('Сьи', 'Śji')

    conv = conv.replace('зья', 'źja')
    conv = conv.replace('зьё', 'źjo')
    conv = conv.replace('зье', 'źje')
    conv = conv.replace('зью', 'źju')
    conv = conv.replace('зьи', 'źji')
    conv = conv.replace('Зья', 'Źja')
    conv = conv.replace('Зьё', 'Źjo')
    conv = conv.replace('Зье', 'Źje')
    conv = conv.replace('Зью', 'Źju')
    conv = conv.replace('Зьи', 'Źji')

    conv = conv.replace('цья', 'ćja')
    conv = conv.replace('цьё', 'ćjo')
    conv = conv.replace('цье', 'ćje')
    conv = conv.replace('цью', 'ćju')
    conv = conv.replace('цьи', 'ćji')
    conv = conv.replace('Цья', 'Ćja')
    conv = conv.replace('Цьё', 'Ćjo')
    conv = conv.replace('Цье', 'Ćje')
    conv = conv.replace('Цью', 'Ćju')
    conv = conv.replace('Цьи', 'Ćji')

    conv = conv.replace("с'я", 'śja')
    conv = conv.replace("з'я", 'źja')
    conv = conv.replace("з'ё", 'źjo')
    conv = conv.replace("з'е", 'źje')
    conv = conv.replace("з'ю", 'źju')
    conv = conv.replace("з'і", 'źji')
    conv = conv.replace("З'я", 'Źja')
    conv = conv.replace("З'ё", 'Źjo')
    conv = conv.replace("З'е", 'Źje')
    conv = conv.replace("З'ю", 'Źju')
    conv = conv.replace("З'і", 'Źji')
    conv = conv.replace("З'Я", 'ŹJA')
    conv = conv.replace("З'Ё", 'ŹJO')
    conv = conv.replace("З'Е", 'ŹJE')
    conv = conv.replace("З'Ю", 'ŹJU')
    conv = conv.replace("З'І", 'ŹJI')

    conv = conv.replace("'я", 'ja')
    conv = conv.replace("'ё", 'jo')
    conv = conv.replace("'е", 'je')
    conv = conv.replace("'ю", 'ju')
    conv = conv.replace("'і", 'ji')
    conv = conv.replace("'Я", 'JA')
    conv = conv.replace("'Ё", 'JO')
    conv = conv.replace("'Е", 'JE')
    conv = conv.replace("'Ю", 'JU')
    conv = conv.replace("'І", 'JI')

    conv = conv.replace('ʼя', 'ja')
    conv = conv.replace('ʼё', 'jo')
    conv = conv.replace('ʼе', 'je')
    conv = conv.replace('ʼю', 'ju')
    conv = conv.replace('ʼі', 'ji')
    conv = conv.replace('ʼЯ', 'JA')
    conv = conv.replace('ʼЁ', 'JO')
    conv = conv.replace('ʼЕ', 'JE')
    conv = conv.replace('ʼЮ', 'JU')
    conv = conv.replace('ʼІ', 'JI')

    conv = conv.replace('iя', 'ija')
    conv = conv.replace('aя', 'aja')
    conv = conv.replace('oя', 'oja')
    conv = conv.replace('uя', 'uja')
    conv = conv.replace('eя', 'eja')

    conv = conv.replace('iе', 'ije')
    conv = conv.replace('aе', 'aje')
    conv = conv.replace('oе', 'oje')
    conv = conv.replace('uе', 'uje')
    conv = conv.replace('eе', 'eje')

    conv = conv.replace('iё', 'ijo')
    conv = conv.replace('aё', 'ajo')
    conv = conv.replace('oё', 'ojo')
    conv = conv.replace('uё', 'ujo')
    conv = conv.replace('eё', 'ejo')

    conv = conv.replace('iю', 'iju')
    conv = conv.replace('aю', 'aju')
    conv = conv.replace('oю', 'oju')
    conv = conv.replace('uю', 'uju')
    conv = conv.replace('eю', 'eju')

    conv = conv.replace('ая', 'aja')
    conv = conv.replace('оя', 'oja')
    conv = conv.replace('уя', 'uja')
    conv = conv.replace('ыя', 'yja')
    conv = conv.replace('ія', 'ija')
    conv = conv.replace('эя', 'eja')
    conv = conv.replace('яя', 'яjа')
    conv = conv.replace('юя', 'юjа')
    conv = conv.replace('ея', 'еjа')
    conv = conv.replace('ёя', 'ёjа')

    conv = conv.replace('ае', 'aje')
    conv = conv.replace('ое', 'oje')
    conv = conv.replace('уе', 'uje')
    conv = conv.replace('ые', 'yje')
    conv = conv.replace('іе', 'ije')
    conv = conv.replace('эе', 'eje')
    conv = conv.replace('яе', 'яje')
    conv = conv.replace('юе', 'юje')
    conv = conv.replace('ее', 'еje')
    conv = conv.replace('ёе', 'ёje')
    conv = conv.replace('Яе', 'Яje')

    conv = conv.replace('аё', 'ajo')
    conv = conv.replace('оё', 'ojo')
    conv = conv.replace('уё', 'ujo')
    conv = conv.replace('ыё', 'yjo')
    conv = conv.replace('іё', 'ijo')
    conv = conv.replace('эё', 'ejo')
    conv = conv.replace('яё', 'яjo')
    conv = conv.replace('юё', 'юjo')
    conv = conv.replace('её', 'еjo')
    conv = conv.replace('ёё', 'ёjo')

    conv = conv.replace('аю', 'aju')
    conv = conv.replace('ою', 'oju')
    conv = conv.replace('ую', 'uju')
    conv = conv.replace('ыю', 'yju')
    conv = conv.replace('ію', 'iju')
    conv = conv.replace('эю', 'eju')
    conv = conv.replace('яю', 'яju')
    conv = conv.replace('юю', 'юju')
    conv = conv.replace('ею', 'еju')
    conv = conv.replace('ёю', 'ёju')
    conv = conv.replace('Ёю', 'Ёju')

    conv = conv.replace('ўя', 'ŭja')
    conv = conv.replace('ўе', 'ŭje')
    conv = conv.replace('ўё', 'ŭjo')
    conv = conv.replace('ўю', 'ŭju')

    conv = conv.replace("'я", "ja")
    conv = conv.replace("'е", "je")
    conv = conv.replace("'ё", "jo")
    conv = conv.replace("'ю", "ju")

    conv = conv.replace('>я', '>ja')
    conv = conv.replace('>е', '>je')
    conv = conv.replace('>ё', '>jo')
    conv = conv.replace('>ю', '>ju')

    conv = conv.replace(';я', ';ja')
    conv = conv.replace(';е', ';je')
    conv = conv.replace(';ё', ';jo')
    conv = conv.replace(';ю', ';ju')
    conv = conv.replace('-я', '-ja')
    conv = conv.replace('-е', '-je')
    conv = conv.replace('-ё', '-jo')
    conv = conv.replace('-ю', '-ju')

    conv = conv.replace('льі', 'lji')
    conv = conv.replace('лья', 'lja')
    conv = conv.replace('лье', 'lje')
    conv = conv.replace('льё', 'ljo')
    conv = conv.replace('лью', 'lju')
    conv = conv.replace('Льі', 'Lji')
    conv = conv.replace('Лья', 'Lja')
    conv = conv.replace('Лье', 'Lje')
    conv = conv.replace('Льё', 'Ljo')
    conv = conv.replace('Лью', 'Lju')

    conv = conv.replace('лі', 'li')
    conv = conv.replace('ль', 'l')
    conv = conv.replace('ля', 'la')
    conv = conv.replace('ле', 'le')
    conv = conv.replace('лё', 'lo')
    conv = conv.replace('лю', 'lu')
    conv = conv.replace('лi', 'li')
    conv = conv.replace('Лі', 'Li')
    conv = conv.replace('Ль', 'L')
    conv = conv.replace('Ля', 'La')
    conv = conv.replace('Ле', 'Le')
    conv = conv.replace('Лё', 'Lo')
    conv = conv.replace('Лю', 'Lu')
    conv = conv.replace('Лi', 'Li')
    conv = conv.replace('ЗЬ', 'Ź')
    conv = conv.replace('СЬ', 'Ś')
    conv = conv.replace('НЬ', 'Ń')
    conv = conv.replace('ЦЬ', 'Ć')
    conv = conv.replace('Зь', 'Ź')
    conv = conv.replace('Сь', 'Ś')
    conv = conv.replace('Нь', 'Ń')
    conv = conv.replace('Ць', 'Ć')
    conv = conv.replace('ТЬ', 'Ť')
    conv = conv.replace('Ть', 'Ť')
    conv = conv.replace('ть', 'ť')
    conv = conv.replace('зь', 'ź')
    conv = conv.replace('сь', 'ś')
    conv = conv.replace('нь', 'ń')
    conv = conv.replace('ць', 'ć')

    conv = conv.replace('цця', 'ćcia')
    conv = conv.replace('ццe', 'ćcie')
    conv = conv.replace('ццю', 'ćciu')
    conv = conv.replace('ццё', 'ćcio')
    conv = conv.replace('цці', 'ćci')
    conv = conv.replace('нне', 'ńnie')
    conv = conv.replace('ння', 'ńnia')
    conv = conv.replace('нню', 'ńniu')
    conv = conv.replace('ннё', 'ńnio')
    conv = conv.replace('нні', 'ńni')

    conv = conv.replace(' я', ' ja')
    conv = conv.replace(' е', ' je')
    conv = conv.replace(' ё', ' jo')
    conv = conv.replace(' ю', ' ju')
    conv = conv.replace('(я', '(ja')
    conv = conv.replace('(е', '(je')
    conv = conv.replace('(ё', '(jo')
    conv = conv.replace('(ю', '(ju')
    conv = conv.replace('«я', '«ja')
    conv = conv.replace('«е', '«je')
    conv = conv.replace('«ё', '«jo')
    conv = conv.replace('«ю', '«ju')

    conv = conv.replace('а', 'a')
    conv = conv.replace('б', 'b')
    conv = conv.replace('в', 'v')
    conv = conv.replace('г', 'h')
    conv = conv.replace('д', 'd')
    conv = conv.replace('е', 'ie')
    conv = conv.replace('ё', 'io')
    conv = conv.replace('ж', 'ž')
    conv = conv.replace('з', 'z')
    conv = conv.replace('и', 'i')
    conv = conv.replace('і', 'i')
    conv = conv.replace('й', 'j')
    conv = conv.replace('к', 'k')
    conv = conv.replace('л', 'ł')
    conv = conv.replace('м', 'm')
    conv = conv.replace('н', 'n')
    conv = conv.replace('о', 'o')
    conv = conv.replace('п', 'p')
    conv = conv.replace('р', 'r')
    conv = conv.replace('с', 's')
    conv = conv.replace('т', 't')
    conv = conv.replace('у', 'u')
    conv = conv.replace('ў', 'ŭ')
    conv = conv.replace('ф', 'f')
    conv = conv.replace('х', 'ch')
    conv = conv.replace('ц', 'c')
    conv = conv.replace('ч', 'č')
    conv = conv.replace('ш', 'š')
    conv = conv.replace('ы', 'y')
    conv = conv.replace('ь', '')
    conv = conv.replace('э', 'e')
    conv = conv.replace('ю', 'iu')
    conv = conv.replace('я', 'ia')
    conv = conv.replace('щ', 'ŝ')
    conv = conv.replace('ъ', "'")
    conv = conv.replace('є', 'e')

    conv = conv.replace('А', 'A')
    conv = conv.replace('Б', 'B')
    conv = conv.replace('В', 'V')
    conv = conv.replace('Г', 'H')
    conv = conv.replace('Д', 'D')
    conv = conv.replace('Е', 'Je')
    conv = conv.replace('Ё', 'Jo')
    conv = conv.replace('Ж', 'Ž')
    conv = conv.replace('З', 'Z')
    conv = conv.replace('И', 'I')
    conv = conv.replace('І', 'I')
    conv = conv.replace('Й', 'J')
    conv = conv.replace('К', 'K')
    conv = conv.replace('Л', 'Ł')
    conv = conv.replace('М', 'M')
    conv = conv.replace('Н', 'N')
    conv = conv.replace('О', 'O')
    conv = conv.replace('П', 'P')
    conv = conv.replace('Р', 'R')
    conv = conv.replace('С', 'S')
    conv = conv.replace('Т', 'T')
    conv = conv.replace('У', 'U')
    conv = conv.replace('Ў', 'Ŭ')
    conv = conv.replace('Ф', 'F')
    conv = conv.replace('Х', 'Ch')
    conv = conv.replace('Ц', 'C')
    conv = conv.replace('Ч', 'Č')
    conv = conv.replace('Ш', 'Š')
    conv = conv.replace('Ы', 'Y')
    conv = conv.replace('Ь', '')
    conv = conv.replace('Э', 'E')
    conv = conv.replace('Ю', 'Ju')
    conv = conv.replace('Я', 'Ja')
    conv = conv.replace('Щ', 'Ŝ')
    conv = conv.replace('Ъ', "'")
    conv = conv.replace('Є', 'E')
    conv = re.sub(
        # Capture group 1: Match a non-word character (anything other than letters, digits, or underscores).
        r'(\W)' +
        # Capture group 2: Match exactly four consecutive spaces.
        r'([ ]{4})' +
        # Capture group 3: Match any sequence of characters (non-greedy).
        r'(.*?)' +
        # Capture group 4: Match exactly four consecutive spaces.
        r'([ ]{4})',
        # match.group(1): Refers to the content of the first captured group, which is the non-word character (the character before the four spaces).
        # match.group(3).upper(): Refers to the content of the third captured group (the enclosed text), and .upper() converts it to uppercase.
        lambda match: match.group(1) + match.group(3).upper(),
        conv)
    # remove spaces added at the beginning
    conv = conv[1:-1]
    return conv
