import pandas as pd

from blvresearch.core.SP500output import ALPHA, ABSRET
from blvresearch.core.sentiment import RTRS_SENTIMENT_ENTITY


def get_corr_between_sent_and_next_DAY_values(entity_id, values):
    sent = RTRS_SENTIMENT_ENTITY[entity_id].dropna()
    dates_with_sentiment = sent.index
    values = values[dates_with_sentiment].shift(-1)
    return values.corr(sent[dates_with_sentiment])

corr_absret = dict()
for k, v in ABSRET.items():
    corr_absret[k] = get_corr_between_sent_and_next_DAY_values(k, v)
corr_absret = pd.Series(corr_absret).dropna()

corr_alpha = dict()
for k, v in ALPHA.items():
    corr_alpha[k] = get_corr_between_sent_and_next_DAY_values(k, v)
corr_alpha = pd.Series(corr_alpha).dropna()
"""
###############################################################################
CORRELATIONS BETWEENT SENTIMENT VALUES AND NEXT DAY ABSRET
###############################################################################
Correlation between day T Reuters Sentiment and day T+1 absolute return:
Out of 560 entities for which we could calculate correlation (for 34 entities
we didn't have returns):
- 240 entities have negative correlation between their sentiment scores and
  absolute returns
- 320 entities have positive correlation
- 0 entities have correlation > 0.5
- 2 entities have correlation > 0.4
- 2 entities have correlation > 0.3
- 5 entities have correlation > 0.2
- 28 entities have correlation > 0.1
- 555 entities have correlation < 0.2
- median correlation is 0.008585940233575248
- mean correlation is 0.0059526221984859441
- std of correlations is 0.06952001759529905
###############################################################################

###############################################################################
CORRELATIONS BETWEENT SENTIMENT VALUES AND NEXT DAY ALPHA
###############################################################################
Correlation between day T Reuters Sentiment and day T+1 alpha:
Out of 560 entities for which we could calculate correlation (for 34 entities
we didn't have alphas):
- 249 entities have negative correlation between their sentiment scores and
  alphas
- 311 entities have positive correlation
- 1 entity has correlation > 0.5
- 1 entity has correlation > 0.4
- 3 entities have correlation > 0.3
- 8 entities have correlation > 0.2
- 28 entities have correlation > 0.1
- 552 entities have correlation < 0.2
- median correlation is 0.005402093685392036
- mean correlation is 0.0080275495226360023
- std of correlations is 0.070854838932701961
"""


def get_corr_between_sent_and_next_WEEK_values(entity_id, values):
    sent = RTRS_SENTIMENT_ENTITY[entity_id].resample('W', how=sum).dropna()
    dates_with_sentiment = sent.index
    values = values.resample('W', how=sum)
    values = values[dates_with_sentiment].shift(-1)
    return values.corr(sent[dates_with_sentiment])

corr_absret = dict()
for k, v in ABSRET.items():
    corr_absret[k] = get_corr_between_sent_and_next_WEEK_values(k, v)
corr_absret = pd.Series(corr_absret).dropna()

corr_alpha = dict()
for k, v in ALPHA.items():
    corr_alpha[k] = get_corr_between_sent_and_next_WEEK_values(k, v)
corr_alpha = pd.Series(corr_alpha).dropna()
"""
###############################################################################
CORRELATIONS BETWEENT SENTIMENT VALUES AND NEXT WEEK ABSRET
###############################################################################
Correlation between week T Reuters Sentiment and week T+1 absolute return:
Out of 560 entities for which we could calculate correlation (for 34 entities
we didn't have returns):
- 253 entities have negative correlation between their sentiment scores and
  absolute returns
- 307 entities have positive correlation
- 1 entity has correlation > 0.5
- 1 entity has correlation > 0.4
- 2 entities have correlation > 0.3
- 11 entities have correlation > 0.2
- 51 entities have correlation > 0.1
- 549 entities have correlation < 0.2
- median correlation is 0.0064263295727018475
- mean correlation is 0.0021317384538038411
- std of correlations is 0.10022458798676161
###############################################################################

###############################################################################
CORRELATIONS BETWEENT SENTIMENT VALUES AND NEXT WEEK ALPHA
###############################################################################
Correlation between week T Reuters Sentiment and week T+1 alpha:
Out of 560 entities for which we could calculate correlation (for 34 entities
we didn't have alphas):
- 276 entities have negative correlation between their sentiment scores and
  alphas
- 284 entities have positive correlation
- 1 entity has correlation > 0.5
- 1 entity has correlation > 0.4
- 6 entities have correlation > 0.3
- 11 entities have correlation > 0.2
- 54 entities have correlation > 0.1
- 549 entities have correlation < 0.2
- median correlation is 0.0024136988228890023
- mean correlation is 0.0039457923428277541
- std of correlations is 0.097036120395571551
###############################################################################
"""


def get_corr_between_sent_and_next_MONTH_values(entity_id, values):
    sent = RTRS_SENTIMENT_ENTITY[entity_id].resample('M', how=sum).dropna()
    dates_with_sentiment = sent.index
    values = values.resample('M', how=sum)
    values = values[dates_with_sentiment].shift(-1)
    return values.corr(sent[dates_with_sentiment])

corr_absret = dict()
for k, v in ABSRET.items():
    corr_absret[k] = get_corr_between_sent_and_next_MONTH_values(k, v)
corr_absret = pd.Series(corr_absret).dropna()

corr_alpha = dict()
for k, v in ALPHA.items():
    corr_alpha[k] = get_corr_between_sent_and_next_MONTH_values(k, v)
corr_alpha = pd.Series(corr_alpha).dropna()
"""
###############################################################################
CORRELATIONS BETWEENT SENTIMENT VALUES AND NEXT MONTH ABSRET
###############################################################################
Correlation between month T Reuters Sentiment and month T+1 absolute return:
Out of 560 entities for which we could calculate correlation (for 34 entities
we didn't have returns):
- 325 entities have negative correlation between their sentiment scores and
  absolute returns
- 235 entities have positive correlation
- 5 entities have correlation > 0.5
- 7 entities have correlation > 0.4
- 11 entities have correlation > 0.3
- 27 entities have correlation > 0.2
- 90 entities have correlation > 0.1
- 533 entities have correlation < 0.2
- median correlation is -0.025154380711005418
- mean correlation is -0.019633260452615636
- std of correlations is 0.16416989366848289
###############################################################################

###############################################################################
CORRELATIONS BETWEENT SENTIMENT VALUES AND NEXT MONTH ALPHA
###############################################################################
Correlation between month T Reuters Sentiment and month T+1 alpha:
Out of 560 entities for which we could calculate correlation (for 34 entities
we didn't have alphas):
- 309 entities have negative correlation between their sentiment scores and
  alphas
- 251 entities have positive correlation
- 5 entities have correlation > 0.5
- 7 entities have correlation > 0.4
- 10 entities have correlation > 0.3
- 40 entities have correlation > 0.2
- 101 entities have correlation > 0.1
- 520 entities have correlation < 0.2
- median correlation is -0.01706781238715196
- mean correlation is -0.013490465205163105
- std of correlations is 0.16480432786654486
###############################################################################
"""
