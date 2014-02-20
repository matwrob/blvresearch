import pandas as pd
from scipy.stats.stats import pearsonr

from blvresearch.core.SP500output import ALPHA, ABSRET
from blvresearch.core.sentiment import RTRS_SENTIMENT_ENTITY


def get_corr_between_sent_and_values_DAILY(entity_id, values):
    temp = RTRS_SENTIMENT_ENTITY[entity_id].dropna()
    dates_with_sentiment = temp.index
    values = values[dates_with_sentiment]
    return pearsonr(values, temp[dates_with_sentiment])

corr_absret = dict()
for k, v in ABSRET.items():
    corr_absret[k] = get_corr_between_sent_and_values_DAILY(k, v)
corr_absret = pd.Series(corr_absret).dropna()

corr_alpha = dict()
for k, v in ALPHA.items():
    corr_alpha[k] = get_corr_between_sent_and_values_DAILY(k, v)
corr_alpha = pd.Series(corr_alpha).dropna()
"""
###############################################################################
CORRELATIONS BETWEEN SENTIMENT VALUES AND ABSRET (DAILY)
###############################################################################
Correlation between daily Reuters Sentiment and daily absolute return:
Out of 560 entities for which we could calculate correlation (for 34 entities
we didn't have returns):
- 45 entities have negative correlation between their sentiment scores and
  absolute returns
- 515 entities have positive correlation
- 5 entities have correlation > 0.5
- 15 entities have correlation > 0.4
- 48 entities have correlation > 0.3
- 130 entities have correlation > 0.2
- 322 entities have correlation > 0.1
- 430 entities have correlation < 0.2
- median correlation is 0.11747342942220265
- mean correlation is 0.1326914767233883
- std of correlations is 0.12169974275754691
###############################################################################

###############################################################################
CORRELATIONS BETWEEN SENTIMENT VALUES AND ALPHA (DAILY)
###############################################################################
Correlation between Reuters Sentiment and alpha:
Out of 560 entities for which we could calculate correlation (for 34 entities
we didn't have alphas):
- 34 entities have negative correlation between their sentiment scores and
  alphas
- 526 entities have positive correlation
- 8 entities have correlation > 0.5
- 22 entities have correlation > 0.4
- 63 entities have correlation > 0.3
- 168 entities have correlation > 0.2
- 370 entities have correlation > 0.1
- 392 entities have correlation < 0.2
- median correlation is 0.1409785419896995
- mean correlation is 0.15402342727414853
- std of correlations is 0.12668505936440796
###############################################################################
"""


def get_corr_between_sent_and_values_WEEKLY(entity_id, values):
    temp = RTRS_SENTIMENT_ENTITY[entity_id].resample('W', how=sum).dropna()
    dates_with_sentiment = temp.index
    values = values.resample('W', how=sum)
    values = values[dates_with_sentiment]
    return values.corr(temp[dates_with_sentiment])

corr_absret = dict()
for k, v in ABSRET.items():
    corr_absret[k] = get_corr_between_sent_and_values_WEEKLY(k, v)
corr_absret = pd.Series(corr_absret).dropna()

corr_alpha = dict()
for k, v in ALPHA.items():
    corr_alpha[k] = get_corr_between_sent_and_values_WEEKLY(k, v)
corr_alpha = pd.Series(corr_alpha).dropna()
"""
###############################################################################
CORRELATIONS BETWEEN SENTIMENT VALUES AND ABSRET (WEEKLY)
###############################################################################
Correlation between weekly Reuters Sentiment and weekly absolute return:
Out of 560 entities for which we could calculate correlation (for 34 entities
we didn't have returns):
- 62 entities have negative correlation between their sentiment scores and
  absolute returns
- 498 entities have positive correlation
- 5 entities have correlation > 0.5
- 23 entities have correlation > 0.4
- 57 entities have correlation > 0.3
- 150 entities have correlation > 0.2
- 350 entities have correlation > 0.1
- 410 entities have correlation < 0.2
- median correlation is 0.1302940051598398
- mean correlation is 0.13965207210682101
- std of correlations is 0.13333251806632465
###############################################################################

###############################################################################
CORRELATIONS BETWEEN SENTIMENT VALUES AND ALPHA (WEEKLY)
###############################################################################
Correlation between weekly Reuters Sentiment and weekly alpha:
Out of 560 entities for which we could calculate correlation (for 34 entities
we didn't have alphas):
- 51 entities have negative correlation between their sentiment scores and
  alphas
- 509 entities have positive correlation
- 4 entities have correlation > 0.5
- 31 entities have correlation > 0.4
- 76 entities have correlation > 0.3
- 198 entities have correlation > 0.2
- 390 entities have correlation > 0.1
- 362 entities have correlation < 0.2
- median correlation is 0.1546217098855978
- mean correlation is 0.16095512304143847
- std of correlations is 0.14190550695700108
###############################################################################
"""


def get_corr_between_sent_and_values_MONTHLY(entity_id, values):
    temp = RTRS_SENTIMENT_ENTITY[entity_id].resample('M', how=sum).dropna()
    dates_with_sentiment = temp.index
    values = values.resample('M', how=sum)
    values = values[dates_with_sentiment]
    return values.corr(temp[dates_with_sentiment])

corr_absret = dict()
for k, v in ABSRET.items():
    corr_absret[k] = get_corr_between_sent_and_values_MONTHLY(k, v)
corr_absret = pd.Series(corr_absret).dropna()

corr_alpha = dict()
for k, v in ALPHA.items():
    corr_alpha[k] = get_corr_between_sent_and_values_MONTHLY(k, v)
corr_alpha = pd.Series(corr_alpha).dropna()
"""
###############################################################################
CORRELATIONS BETWEEN SENTIMENT VALUES AND ABSRET (MONTHLY)
###############################################################################
Correlation between monthly Reuters Sentiment and monthly absolute returns:
Out of 560 entities for which we could calculate correlation (for 34 entities
we didn't have returns):
- 51 entities have negative correlation between their sentiment scores and
  absolute returns
- 509 entities have positive correlation
- 19 entities have correlation > 0.5
- 56 entities have correlation > 0.4
- 118 entities have correlation > 0.3
- 275 entities have correlation > 0.2
- 427 entities have correlation > 0.1
- 285 entities have correlation < 0.2
- median correlation is 0.19746257006797113
- mean correlation is 0.19789236566434973
- std of correlations is 0.17137092757749375
###############################################################################

###############################################################################
CORRELATIONS BETWEEN SENTIMENT VALUES AND ALPHAS (MONTHLY)
###############################################################################
Correlation between monthly Reuters Sentiment and monthly alpha:
Out of 560 entities for which we could calculate correlation (for 34 entities
we didn't have alphas):
- 74 entities have negative correlation between their sentiment scores and
  alphas
- 486 entities have positive correlation
- 22 entities have correlation > 0.5
- 53 entities have correlation > 0.4
- 122 entities have correlation > 0.3
- 252 entities have correlation > 0.2
- 387 entities have correlation > 0.1
- 308 entities have correlation < 0.2
- median correlation is 0.1814657376375757
- mean correlation is 0.18268090034910719
- std of correlations is 0.18294814911448226
###############################################################################
"""
