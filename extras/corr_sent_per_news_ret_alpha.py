import pandas as pd

from blvresearch.core.SP500output import ALPHA, ABSRET
from blvresearch.core.sentiment import RTRS_SENTIMENT_ENTITY, RTRS_COUNT_ENTITY


def get_corr_between_avg_sent_and_values_DAILY(entity_id, values):
    sent = RTRS_SENTIMENT_ENTITY[entity_id].dropna()
    dates_with_sentiment = sent.index
    count = RTRS_COUNT_ENTITY[entity_id][sent.index]
    avg_sent = sent / count
    values = values[dates_with_sentiment]
    return values.corr(avg_sent[dates_with_sentiment])

corr_absret = dict()
for k, v in ABSRET.items():
    corr_absret[k] = get_corr_between_avg_sent_and_values_DAILY(k, v)
corr_absret = pd.Series(corr_absret).dropna()

corr_alpha = dict()
for k, v in ALPHA.items():
    corr_alpha[k] = get_corr_between_avg_sent_and_values_DAILY(k, v)
corr_alpha = pd.Series(corr_alpha).dropna()
"""
###############################################################################
CORRELATIONS BETWEEN SENTIMENT SCORE (PER NEWS) AND ABSRET (DAILY)
###############################################################################
Correlation between daily Reuters Sentiment (per news) and daily absolute
returns:
Out of 560 entities for which we could calculate correlation (for 34 entities
we didn't have returns):
- 45 entities have negative correlation between their sentiment scores and
  absolute returns
- 515 entities have positive correlation
- 0 entities have correlation > 0.5
- 1 entities have correlation > 0.4
- 4 entities have correlation > 0.3
- 21 entities have correlation > 0.2
- 185 entities have correlation > 0.1
- 539 entities have correlation < 0.2
- median correlation is 0.07325270591943259
- mean correlation is 0.07502388708982019
- std of correlations is 0.084770318695462199
###############################################################################

###############################################################################
CORRELATIONS BETWEEN SENTIMENT SCORE (PER NEWS) AND ALPHA (DAILY)
###############################################################################
Correlation between daily Reuters Sentiment (per news) and daily alpha:
Out of 560 entities for which we could calculate correlation (for 34 entities
we didn't have alphas):
- 35 entities have negative correlation between their sentiment scores and
  alphas
- 525 entities have positive correlation
- 0 entities have correlation > 0.5
- 0 entities have correlation > 0.4
- 3 entities have correlation > 0.3
- 26 entities have correlation > 0.2
- 226 entities have correlation > 0.1
- 534 entities have correlation < 0.2
- median correlation is 0.08427580850958362
- mean correlation is 0.086222890302154007
- std of correlations is 0.086222890302154007
###############################################################################
"""


def get_corr_between_avg_sent_and_values_WEEKLY(entity_id, values):
    sent = RTRS_SENTIMENT_ENTITY[entity_id].resample('W', how=sum).dropna()
    dates_with_sentiment = sent.index
    count = RTRS_COUNT_ENTITY[entity_id].resample('W', how=sum)[sent.index]
    avg_sent = sent / count
    values = values.resample('W', how=sum)
    values = values[dates_with_sentiment]
    return values.corr(avg_sent[dates_with_sentiment])

corr_absret = dict()
for k, v in ABSRET.items():
    corr_absret[k] = get_corr_between_avg_sent_and_values_WEEKLY(k, v)
corr_absret = pd.Series(corr_absret).dropna()

corr_alpha = dict()
for k, v in ALPHA.items():
    corr_alpha[k] = get_corr_between_avg_sent_and_values_WEEKLY(k, v)
corr_alpha = pd.Series(corr_alpha).dropna()
"""
###############################################################################
CORRELATIONS BETWEEN SENTIMENT SCORE (PER NEWS) AND ABSRET (WEEKLY)
###############################################################################
Correlation between weekly Reuters Sentiment (per news) and weekly absolute
returns:
Out of 560 entities for which we could calculate correlation (for 34 entities
we didn't have returns):
- 63 entities have negative correlation between their sentiment scores and
  absolute returns
- 497 entities have positive correlation
- 0 entities have correlation > 0.5
- 2 entities have correlation > 0.4
- 8 entities have correlation > 0.3
- 40 entities have correlation > 0.2
- 221 entities have correlation > 0.1
- 520 entities have correlation < 0.2
- median correlation is 0.08435341581104022
- mean correlation is 0.083051307234665681
- std of correlations is 0.09484217832337892
###############################################################################

###############################################################################
CORRELATIONS BETWEEN SENTIMENT SCORE (PER NEWS) AND ALPHA (WEEKLY)
###############################################################################
Correlation between weekly Reuters Sentiment (per news) and weekly alpha:
Out of 560 entities for which we could calculate correlation (for 34 entities
we didn't have alphas):
- 50 entities have negative correlation between their sentiment scores and
  alphas
- 510 entities have positive correlation
- 0 entities have correlation > 0.5
- 1 entities have correlation > 0.4
- 9 entities have correlation > 0.3
- 51 entities have correlation > 0.2
- 276 entities have correlation > 0.1
- 509 entities have correlation < 0.2
- median correlation is 0.09723424873198631
- mean correlation is 0.095261549609063356
- std of correlations is 0.092970102657996614
###############################################################################
"""


def get_corr_between_avg_sent_and_values_MONTHLY(entity_id, values):
    sent = RTRS_SENTIMENT_ENTITY[entity_id].resample('M', how=sum).dropna()
    dates_with_sentiment = sent.index
    count = RTRS_COUNT_ENTITY[entity_id].resample('M', how=sum)[sent.index]
    avg_sent = sent / count
    values = values.resample('M', how=sum)
    values = values[dates_with_sentiment]
    return values.corr(avg_sent[dates_with_sentiment])

corr_absret = dict()
for k, v in ABSRET.items():
    corr_absret[k] = get_corr_between_avg_sent_and_values_MONTHLY(k, v)
corr_absret = pd.Series(corr_absret).dropna()

corr_alpha = dict()
for k, v in ALPHA.items():
    corr_alpha[k] = get_corr_between_avg_sent_and_values_MONTHLY(k, v)
corr_alpha = pd.Series(corr_alpha).dropna()
"""
###############################################################################
CORRELATIONS BETWEEN SENTIMENT SCORE (PER NEWS) AND ABSRET (MONTHLY)
###############################################################################
Correlation between monthly Reuters Sentiment (per news) and monthly absolute
returns:
Out of 560 entities for which we could calculate correlation (for 34 entities
we didn't have returns):
- 58 entities have negative correlation between their sentiment scores and
  absolute returns
- 502 entities have positive correlation
- 6 entities have correlation > 0.5
- 11 entities have correlation > 0.4
- 41 entities have correlation > 0.3
- 160 entities have correlation > 0.2
- 375 entities have correlation > 0.1
- 400 entities have correlation < 0.2
- median correlation is 0.14622498812697732
- mean correlation is 0.14048144284341818
- std of correlations is 0.15381726093091391
###############################################################################

##############################################################################
CORRELATIONS BETWEEN SENTIMENT SCORE (PER NEWS) AND ALPHA (MONTHLY)
##############################################################################
Correlation between monthly Reuters Sentiment (per news) and monthly alpha:
Out of 560 entities for which we could calculate correlation (for 34 entities
we didn't have alphas):
- 76 entities have negative correlation between their sentiment scores and
  alphas
- 484 entities have positive correlation
- 5 entities have correlation > 0.5
- 14 entities have correlation > 0.4
- 36 entities have correlation > 0.3
- 161 entities have correlation > 0.2
- 336 entities have correlation > 0.1
- 399 entities have correlation < 0.2
- median correlation is 0.12719692575825617
- mean correlation is 0.12613045862470829
- std of correlations is 0.15474267887845497
###############################################################################
"""
