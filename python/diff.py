
from dataclasses import dataclass
import itertools
import os
import sys
import tempfile
import difflib

import requests
from bs4 import BeautifulSoup
from belorthography import engine, diff_mode, cases

@dataclass
class Sample:
    """Sample data for testing. Should point to a text or html file on the web."""
    name: str
    url: str
    orthography: cases.Case

SAMPLES = [
    Sample(
        name = 'long_way_home',
        url = 'https://knihi.com/Vasil_Bykau/Douhaja_daroha_dadomu.html',
        orthography = cases.Case.CYR_TARAS,
    ),
    Sample(
        name = 'charnobylskaja_malitva',
        url = 'https://knihi.com/Sviatlana_Aleksijevic/Carnobylskaja_malitva.html',
        orthography = cases.Case.CYR_NAR
    ),
]

def maybe_cache_file(name: str, url: str):
    """If the file is not cached, download it and cache it"""
    if not os.path.exists(name):
        with open(name, 'w') as f:
            r = requests.get(url)
            html = r.content.decode('utf-8')
            f.write(BeautifulSoup(html, 'html.parser').get_text())

def read_file_from_url(sample: Sample) -> str:
    """Read the file from the given URL and return the contents as a string"""
    full_name = tempfile.gettempdir() + '/' + sample.name + '.txt'
    maybe_cache_file(full_name, sample.url)
    return open(full_name, 'r').read()

def process_sample(sample: Sample):
    cyr = read_file_from_url(sample)

    diff_mode.set_new(False)
    lac_golden = engine.convert(cyr, sample.orthography, engine.Case.LAT)

    diff_mode.set_new(True)
    lac_new = engine.convert(cyr, sample.orthography, engine.Case.LAT)
    if lac_golden == lac_new:
        print(f"{sample.name}: OK")
    else:
        cyr_lines = cyr.splitlines()
        empty_lines = [''] * len(cyr_lines)
        golden_lines = lac_golden.splitlines()
        golden_lines = list(itertools.chain(*zip(empty_lines, cyr_lines, golden_lines)))
        new_lines = lac_new.splitlines()
        new_lines = list(itertools.chain(*zip(empty_lines, cyr_lines, new_lines)))

        diff = difflib.HtmlDiff().make_file(golden_lines, new_lines, "Golden", "New")
        # Remove no wrap and set max with to ~half screen so that lon lines are wrapped.
        # Also replaces non-breaking spaces with regular spaces to achieve wrapping.
        diff = diff.replace('nowrap="nowrap"', '')
        diff = diff.replace('<head>', '<head><style>td { max-width: 45vw; } </style>')
        diff = diff.replace('&nbsp;', ' ')
        diff_file = tempfile.gettempdir() + '/' + sample.name + '.diff.html'
        with open(diff_file, 'w') as f:
            f.write(diff)
        print(f"{sample.name}: DIFF file://{diff_file}")



def main() -> int:
    for sample in SAMPLES:
        process_sample(sample)
    return 0

if __name__ == '__main__':
    sys.exit(main())