import pytest

from belorthography import convert, Orthography


def test_unsupported():
    with pytest.raises(
        ValueError, match=r"Conversion from LATIN to CLASSICAL is not supported."
    ):
        convert("foo", Orthography.LATIN, Orthography.CLASSICAL)
