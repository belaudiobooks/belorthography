"""
This module implements diff mode for testing conversion algorithms.
It provides public function is_new() that can be used in conversion
code to check whether code has any effect on the oputput.

Check "Diff mode" sexion in README.md for more details.
"""
import os

# DIFF_NEW allows to override the value when running unit tests.
_new = os.environ.get('DIFF_NEW', 'false').lower() == 'true'

def is_new():
    """Check if diff mode is enabled and new code should be invoked."""
    return _new

def set_new(val):
    """Sets diff mode. Should be called only from diff.py."""
    global _new
    _new = val