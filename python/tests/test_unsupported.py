import pytest

from belorthography import convert, Case

def test_unsupported():
    with pytest.raises(ValueError, match=r'Conversion from LAT to CYR_TARAS is not supported.'):
        convert("foo", Case.LAT, Case.CYR_TARAS)
