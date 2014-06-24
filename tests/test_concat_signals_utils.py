import pandas as pd
import numpy as np
import unittest

from blvresearch.concat.signals.utils import (
    remove_consecutive_values
)


MOCK_SERIES = pd.Series([False, False, False, pd.np.nan, True, True,
                         False, False, True, False, pd.np.nan, False, True],
                         index=pd.DatetimeIndex(freq='B',
                                                start='2013-06-15',
                                                end='2013-07-03'))


class TestRemoveConsecutiveValues(unittest.TestCase):

    def test_series(self):
        res = remove_consecutive_values(MOCK_SERIES)
        exp = pd.Series({'2013-06-17': False,
                         '2013-06-21': True,
                         '2013-06-25': False,
                         '2013-06-27': True,
                         '2013-06-28': False,
                         '2013-07-03': True})
        np.testing.assert_array_equal(res, exp)
