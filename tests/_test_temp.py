

INDEX = pd.MultiIndex.from_tuples(
    [v for v in product(['012ABC-D', '123BCD-E', '234CDE-F'],
                        pd.date_range('2003-01-02', '2003-03-31', freq='B'))]
)
DATA = ([[1, 2, 3]] * 21 + [[2, 3, 4]] * 21 + [[3, 4, 5]] * 21 +
        [[5, 4, 3]] * 21 + [[4, 3, 2]] * 21 + [[3, 2, 1]] * 21 +
        [[0, 3, 1]] * 21 + [[6, 4, 2]] * 21 + [[3, 6, 9]] * 21)
COLUMNS = ['abs_ret', 'rel_ret', 'alpha']
MOCK_OUTPUT = pd.DataFrame(data=DATA, index=INDEX, columns=COLUMNS)


INDEX = pd.DatetimeIndex(pd.date_range('2003-01-02', '2003-03-31', freq='B'))
DATA = ([[1, 2, 3]] * 21 + [[2, 3, 4]] * 21 + [[3, 4, 5]] * 21 +
        [[5, 4, 3]] * 21 + [[4, 3, 2]] * 21 + [[3, 2, 1]] * 21 +
        [[0, 3, 1]] * 21 + [[6, 4, 2]] * 21 + [[3, 6, 9]] * 21)
COLUMNS = ['Stock1', 'Stock2', 'Stock3']
MOCK_RETURNS = pd.DataFrame(data=DATA, index=INDEX, columns=COLUMNS)


class TestPortfolioStrategy(unittest.TestCase):

    class MockStrategy(PortfolioStrategy):
        HOLDING_PERIODS = 2
        PAUSE_PERIODS = 1
        REBALANCING_FREQUENCY = 'W-FRI'
        PORTFOLIO_SIZE = 20

        def _get_positions(self):
            all_entities = list(set(self.output.index.get_level_values(0)))
            result = dict()
            for day in self.rebalancing_days:
                result[day] = all_entities[:self.PORTFOLIO_SIZE]
            return pd.Series(result)

    STRATEGY = MockStrategy(MOCK_OUTPUT)

    def test_positions(self):
        self.assertIsInstance(self.STRATEGY.positions, pd.TimeSeries)

        exp = self.STRATEGY.rebalancing_days
        pd.np.testing.assert_array_equal(self.STRATEGY.positions.index, exp)

        for k, v in self.STRATEGY.positions.items():
            self.assertIsInstance(k, pd.tslib.Timestamp)
            self.assertIsInstance(v, list)

    def test_ranking_days(self):
        expected = ['2003-01-03', '2003-01-17', '2003-01-31', '2003-02-14',
                    '2003-02-28', '2003-03-14']
        for i, d in enumerate(expected):
            result = self.STRATEGY.ranking_days[i]
            self.assertEqual(d, result.strftime('%Y-%m-%d'))

    def test_rebalancing_days(self):
        expected = ['2003-01-10', '2003-01-24', '2003-02-07', '2003-02-21',
                    '2003-03-07', '2003-03-21']
        for i, d in enumerate(expected):
            result = self.STRATEGY.rebalancing_days[i]
            self.assertEqual(d, result.strftime('%Y-%m-%d'))



INDEX2 = pd.MultiIndex.from_tuples(
    [v for v in product(['012ABC-D', '123BCD-E', '234CDE-F'],
                        pd.date_range('2003-01-02', '2003-03-31', freq='B'))]
)
DATA2 = ([[1, 2, 3]] * 21 + [[2, 3, 4]] * 21 + [[3, 4, 5]] * 21 +
         [[5, 4, 3]] * 21 + [[4, 3, 2]] * 21 + [[3, 2, 1]] * 21 +
         [[0, 3, 1]] * 21 + [[6, 4, 2]] * 21 + [[3, 6, 9]] * 21)
COLUMNS2 = ['abs_ret', 'rel_ret', 'alpha']
MOCK_OUTPUT2 = pd.DataFrame(data=DATA2, index=INDEX2, columns=COLUMNS2)
