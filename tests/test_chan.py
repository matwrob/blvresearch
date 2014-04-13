import pandas as pd
import unittest

from blvresearch.core.chan import (
    ChanNewsReturns, ChanNoNewsReturns
)

from concat.core.utils import load_object


RESEARCH_DATA = load_object('/vagrant/blvresearch/tests/mock_jegadeesh.pickle')

def ts(year, month, day):
    dt = pd.datetime(year, month, day, 0, 0, 0)
    return pd.Timestamp(dt, tz='UTC')


class TestChanNewsReturns(unittest.TestCase):

    CNR = ChanNewsReturns(RESEARCH_DATA,
                          type_of_returns='alpha',
                          no_of_quantiles=3)

    def test_nan_returns_without_news(self):
        returns = self.CNR._get_initial_returns(freq='M')
        result = self.CNR._nan_returns_without_news(returns)
