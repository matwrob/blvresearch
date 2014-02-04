class NoOfNewsPortfolio(DynamicBacktest):

    def _get_starting_points_and_holdings(self):
        news = self.o['news'].dropna()
        news_amount = {k: news[v].map(len).sum(level=1)
                       for k, v in SECTOR_MEMBERS.items()}
        mean_news_amount = {k: v / len(SECTOR_MEMBERS[k])
                            for k, v in news_amount_per_sector.items()}
        mean_news_amount = pd.DataFrame(mean_news_amount)
        mean_news_amount = mean_news_amount.resample('W-SUN', how='sum')
        result = dict()
        for k, v in mean_news_amount.iterrows():
            result[k] = SECTOR_MEMBERS[v.idxmax()]
        last_date = mean_news.index[-1 - self.hold_per]
        return pd.Series(result)[:last_date]
