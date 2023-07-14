#!/usr/bin/env python
from setuptools import setup

setup(
    name="translit",
    version="0.0.1b0",
    author="audiobooks.by",
    description="Libraries for converting Belarusian cyrillic text to lacinka.",
    license="MIT",
    keywords="Belarusian cyrillic lacinka",
    packages=['translit', 'tests'],
    classifiers=[
        "Development Status :: 0 - Beta",
    ],
)
