import pandas as pd
import numpy as np
import unittest

from blvresearch.concat.signals.news_based.news_signals_take0 import (
    _get_rows
)

PATH = 'blvresearch/tests/mock_ubs_data/ubs_alpha.csv'

MOCK_DATA = pd.DataFrame({'alpha': pd.Series.from_csv(PATH)})


class TestGetRows(unittest.TestCase):

    def test_get(self):
        res0, res1, res2 = _get_rows(MOCK_DATA.index[1], MOCK_DATA)
        self.assertEqual(str(res0.index),
                         '2012-06-19')
        self.assertEqual(str(res1.index),
                         '2012-06-20')
        self.assertEqual(str(res2.index),
                         '2012-06-21')

    def test_get(self):
        res0, res1, res2 = _get_rows(MOCK_DATA.index[2], MOCK_DATA)
        self.assertEqual(str(res0.index),
                         '2012-06-20')
        self.assertEqual(str(res1.index),
                         '2012-06-21')
        self.assertEqual(str(res2.index),
                         '2012-06-22')
