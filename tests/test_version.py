from os import path
import sys

try:
    thisdir = path.dirname(path.abspath(__file__))
    sys.path.append(path.join(thisdir, '..'))
except Exception:                       # noqa: PIE786
    sys.path.append('..')


def test_version():
    """Test version import."""
    from commonpy import __version__
    assert __version__
