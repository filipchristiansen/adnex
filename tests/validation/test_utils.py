""" Tests for the validation module. """

import pandas as pd

from adnex.validation.utils import _is_integer, has_ca125


def test_has_ca125():
    assert has_ca125(pd.Series({'s_ca_125': 50}))
    assert has_ca125(pd.Series({'s_ca_125': 0}))
    assert has_ca125(pd.Series({'s_ca_125': -1}))
    assert not has_ca125(pd.Series({}))
    assert not has_ca125(pd.Series({'s_ca_125': None}))


def test_is_integer():
    assert _is_integer(1)
    assert _is_integer(0)
    assert _is_integer(-1)
    assert _is_integer(1.0)
    assert not _is_integer(1.1)
    assert not _is_integer(-1.1)
    assert not _is_integer('1')
    assert not _is_integer('1.1')
    assert not _is_integer('a')
    assert not _is_integer(None)
