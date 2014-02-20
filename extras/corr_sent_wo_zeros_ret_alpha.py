import pandas as pd

from blvresearch.core.sentiment import RTRS_SENTIMENT_ENTITY
from blvresearch.core.SP500output import ABSRET, ALPHA


def get_corr_between_sent_wo_0_and_values_DAILY(entity_id, values):
    temp = RTRS_SENTIMENT_ENTITY[entity_id].dropna()
    dates_with_sentiment = temp[temp != 0].index
    values = values[dates_with_sentiment]
    return values.corr(temp[dates_with_sentiment])

corr_absret_wo_0 = dict()
for k, v in ABSRET.items():
    corr_absret_wo_0[k] = get_corr_between_sent_wo_0_and_values_DAILY(k, v)
corr_absret_wo_0 = pd.Series(corr_absret_wo_0).dropna()

corr_alpha_wo_0 = dict()
for k, v in ALPHA.items():
    corr_alpha_wo_0[k] = get_corr_between_sent_wo_0_and_values_DAILY(k, v)
corr_alpha_wo_0 = pd.Series(corr_alpha_wo_0).dropna()
"""
###############################################################################
CORRELATIONS BETWEEN NON-ZERO SENTIMENT VALUES AND ABSRET (DAILY)
###############################################################################
Correlation between daily Reuters Sentiment (zero sentiment days are discarded)
and absolute return:
Out of 560 entities for which we could calculate correlation (for 34 entities
we didn't have returns):
- 45 entities have negative correlation between their sentiment scores and
  absolute returns
- 515 entities have positive correlation
- 5 entities have correlation > 0.5
- 16 entities have correlation > 0.4
- 49 entities have correlation > 0.3
- 140 entities have correlation > 0.2
- 326 entities have correlation > 0.1
- 420 entities have correlation < 0.2
- median correlation is 0.11980645902116119
- mean correlation is 0.13532090846351083
- std of correlations is 0.12275723610595501
###############################################################################

###############################################################################
CORRELATIONS BETWEEN NON-ZERO SENTIMENT VALUES AND ALPHA (DAILY)
###############################################################################
Correlation between daily Reuters Sentiment (zero sentiment days are discarded)
and alphas:
Out of 560 entities for which we could calculate correlation (for 34 entities
we didn't have alphas):
- 34 entities have negative correlation between their sentiment scores and
  alphas
- 526 entities have positive correlation
- 9 entities have correlation > 0.5
- 23 entities have correlation > 0.4
- 66 entities have correlation > 0.3
- 174 entities have correlation > 0.2
- 374 entities have correlation > 0.1
- 386 entities have correlation < 0.2
- median correlation is 0.14329697151891535
- mean correlation is 0.15646438802060125
- std of correlations is 0.12816591628152768
###############################################################################
"""


def get_corr_between_sent_wo_0_and_values_WEEKLY(entity_id, values):
    temp = RTRS_SENTIMENT_ENTITY[entity_id].resample('W', how=sum).dropna()
    dates_with_sentiment = temp[temp != 0].index
    values = values.resample('W', how=sum)
    values = values[dates_with_sentiment]
    return values.corr(temp[dates_with_sentiment])

corr_absret_wo_0 = dict()
for k, v in ABSRET.items():
    corr_absret_wo_0[k] = get_corr_between_sent_wo_0_and_values_WEEKLY(k, v)
corr_absret_wo_0 = pd.Series(corr_absret_wo_0).dropna()

corr_alpha_wo_0 = dict()
for k, v in ALPHA.items():
    corr_alpha_wo_0[k] = get_corr_between_sent_wo_0_and_values_WEEKLY(k, v)
corr_alpha_wo_0 = pd.Series(corr_alpha_wo_0).dropna()
"""
###############################################################################
CORRELATIONS BETWEEN NON-ZERO SENTIMENT VALUES AND ABSRET (WEEKLY)
###############################################################################
Correlation between weekly Reuters Sentiment (zero sentiment weeks are
discarded) and absolute returns:
Out of 560 entities for which we could calculate correlation (for 34 entities
we didn't have returns):
- 62 entities have negative correlation between their sentiment scores and
  absolute returns
- 498 entities have positive correlation
- 7 entities have correlation > 0.5
- 24 entities have correlation > 0.4
- 57 entities have correlation > 0.3
- 154 entities have correlation > 0.2
- 358 entities have correlation > 0.1
- 406 entities have correlation < 0.2
- median correlation is 0.13346141487583796
- mean correlation is 0.14245696406876465
- std of correlations is 0.13682306642216607
###############################################################################

###############################################################################
CORRELATIONS BETWEEN NON-ZERO SENTIMENT VALUES AND ALPHA (WEEKLY)
###############################################################################
Correlation between weekly Reuters Sentiment (zero sentiment weeks are
discarded) and alphas:
Out of 560 entities for which we could calculate correlation (for 34 entities
we didn't have alphas):
- 51 entities have negative correlation between their sentiment scores and
  alphas
- 509 entities have positive correlation
- 5 entities have correlation > 0.5
- 33 entities have correlation > 0.4
- 78 entities have correlation > 0.3
- 208 entities have correlation > 0.2
- 388 entities have correlation > 0.1
- 352 entities have correlation < 0.2
- median correlation is 0.1572212305850711
- mean correlation is 0.16369146788267158
- std of correlations is 0.14602248958789038
###############################################################################
"""


def get_corr_between_sent_wo_0_and_values_MONTHLY(entity_id, values):
    temp = RTRS_SENTIMENT_ENTITY[entity_id].resample('M', how=sum).dropna()
    dates_with_sentiment = temp[temp != 0].index
    values = values.resample('M', how=sum)
    values = values[dates_with_sentiment]
    return values.corr(temp[dates_with_sentiment])

corr_absret_wo_0 = dict()
for k, v in ABSRET.items():
    corr_absret_wo_0[k] = get_corr_between_sent_wo_0_and_values_MONTHLY(k, v)
corr_absret_wo_0 = pd.Series(corr_absret_wo_0).dropna()

corr_alpha_wo_0 = dict()
for k, v in ALPHA.items():
    corr_alpha_wo_0[k] = get_corr_between_sent_wo_0_and_values_MONTHLY(k, v)
corr_alpha_wo_0 = pd.Series(corr_alpha_wo_0).dropna()
"""
###############################################################################
CORRELATIONS BETWEEN NON-ZERO SENTIMENT VALUES AND ABSRET (MONTHLY)
###############################################################################
Correlation between monthly Reuters Sentiment (zero sentiment months are
discarded) and absolute returns:
Out of 560 entities for which we could calculate correlation (for 34 entities
we didn't have returns):
- 51 entities have negative correlation between their sentiment scores and
  absolute returns
- 509 entities have positive correlation
- 19 entities have correlation > 0.5
- 59 entities have correlation > 0.4
- 121 entities have correlation > 0.3
- 279 entities have correlation > 0.2
- 427 entities have correlation > 0.1
- 281 entities have correlation < 0.2
- median correlation is 0.1997230552274773
- mean correlation is 0.19890578864188407
- std of correlations is 0.17250715902597366
###############################################################################

###############################################################################
CORRELATIONS BETWEEN NON-ZERO SENTIMENT VALUES AND ALPHA (MONTHLY)
###############################################################################
Correlation between monthly Reuters Sentiment (zero sentiment months are
discarded) and alphas:
Out of 560 entities for which we could calculate correlation (for 34 entities
we didn't have alphas):
- 75 entities have negative correlation between their sentiment scores and
  alphas
- 485 entities have positive correlation
- 22 entities have correlation > 0.5
- 53 entities have correlation > 0.4
- 124 entities have correlation > 0.3
- 253 entities have correlation > 0.2
- 389 entities have correlation > 0.1
- 307 entities have correlation < 0.2
- median correlation is 0.18238508372161294
- mean correlation is 0.18339388081089275
- std of correlations is 0.18374353855917594
###############################################################################
"""
