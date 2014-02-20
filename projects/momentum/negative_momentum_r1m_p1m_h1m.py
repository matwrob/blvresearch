from blvresearch.core.portfolio import (
    Portfolio, PortfolioCharacteristics, BOTTOM_DECILE
)
from blvresearch.projects.momentum.positive_momentum_r1m_p1m_h1m import (
    PositiveSentiment_1M_1M_1M, PositiveMomentum_1M_1M_1M,
    PositiveAlphaMomentum_1M_1M_1M, PositiveImpDays_1M_1M_1M
)
from blvresearch.core.sentiment import RTRS_SENTIMENT_ENTITY
from blvresearch.core.SP500output import ABSRET, ALPHA, NEWS


class NegativeSentiment_1M_1M_1M(PositiveSentiment_1M_1M_1M):

    NAME = 'Negative sentiment score based momentum'

    def _get_decile(self, series):
        return BOTTOM_DECILE(series, self.PORTFOLIO_SIZE)


neg_sent_strat = NegativeSentiment_1M_1M_1M(
    ABSRET, supplementary_data=RTRS_SENTIMENT_ENTITY
)
neg_sent_port = Portfolio(neg_sent_strat)
neg_sent_perf = neg_sent_port.daily_performance()
neg_sent_perf.name = 'Negative sentiment score momentum'
neg_sent_char = PortfolioCharacteristics(neg_sent_port)


class NegativeMomentum_1M_1M_1M(PositiveMomentum_1M_1M_1M):

    def _get_decile(self, series):
        return BOTTOM_DECILE(series, self.PORTFOLIO_SIZE)


neg_mom_strat = NegativeMomentum_1M_1M_1M(ABSRET)
neg_mom_port = Portfolio(neg_mom_strat)
neg_mom_perf = neg_mom_port.daily_performance()
neg_mom_perf.name = 'Negative momentum'
neg_mom_char = PortfolioCharacteristics(neg_mom_port)


class NegativeAlphaMomentum_1M_1M_1M(PositiveAlphaMomentum_1M_1M_1M):

    def _get_decile(self, series):
        return BOTTOM_DECILE(series, self.PORTFOLIO_SIZE)


neg_alpha_strat = NegativeAlphaMomentum_1M_1M_1M(
    ABSRET,
    supplementary_data=ALPHA
)
neg_alpha_port = Portfolio(neg_alpha_strat)
neg_alpha_perf = neg_alpha_port.daily_performance()
neg_alpha_perf.name = 'Negative alpha momentum'
neg_alpha_char = PortfolioCharacteristics(neg_alpha_port)


class NegativeImpDays_1M_1M_1M(PositiveImpDays_1M_1M_1M):

    NAME = """Considers only stocks that experienced important day within
              the ranking period and ranking period return was negative"""

    def _get_decile(self, series):
        return BOTTOM_DECILE(series, self.PORTFOLIO_SIZE)


neg_imp_days_strat = NegativeImpDays_1M_1M_1M(
    ABSRET, supplementary_data={'news': NEWS, 'alpha': ALPHA}
)
neg_imp_days_port = Portfolio(neg_imp_days_strat)
neg_imp_days_perf = neg_imp_days_port.daily_performance()
neg_imp_days_perf.name = 'Important day based momentum'
neg_imp_days_char = PortfolioCharacteristics(neg_imp_days_port)
