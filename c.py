import pandas as pd

from blvresearch.core.SP500output import NEWS, ALPHA, ABSRET
from blvresearch.core.sentiment import RTRS_SENTIMENT_ENTITY, RTRS_COUNT_ENTITY

from concat.core.news import NewsList

has_news = NEWS.applymap(lambda x: isinstance(x, NewsList))


sent_stats = pd.DataFrame(index=RTRS_SENTIMENT_ENTITY.columns,
                          columns=['days_pos', 'days_neg', 'days_neut'])
for k, v in RTRS_SENTIMENT_ENTITY.items():
    temp = v.dropna()
    sent_stats['days_pos'][k] = len(temp[temp > 0]) / len(temp)
    sent_stats['days_neg'][k] = len(temp[temp < 0]) / len(temp)
    sent_stats['days_neut'][k] = len(temp[temp == 0]) / len(temp)

"""
###########################################
STATISTICS ON SENTIMENT ACROSS 594 ENTITIES
###########################################
Percentage of all days with sentiment scores that are:
NEUTRAL:
- median of percentage of days with NEUTRAL sentiment: 8.6 %
- mean of number of days with NEUTRAL sentiment: 9.0 %
- std of number of days with NEUTRAL sentiment: 4.6 %

POSITIVE:
- median of percentage of days with NEUTRAL sentiment: 46.7 %
- mean of number of days with NEUTRAL sentiment: 47.0 %
- std of number of days with NEUTRAL sentiment: 10.5 %

NEGATIVE:
- median of percentage of days with NEUTRAL sentiment: 44.3 %
- mean of number of days with NEUTRAL sentiment: 44.1 %
- std of number of days with NEUTRAL sentiment: 11.4 %
"""

more_negative = sent_stats.T.apply(lambda x: x['days_neg'] > x['days_pos'])
"""
There are 269 entities with more days with negative sentiment than positive
There are 325 entities with more days with positive sentiment thant negative
"""

"""
How does this relate to ABSRET and ALPHA? What percentage of days on average
(across all entities) is positive/negative/neutral abolute return days or
positive/negative/neutral alpha days?

"""
absret_stats = pd.DataFrame(index=ABSRET.columns,
                            columns=['days_pos', 'days_neg', 'days_neut'])
for k, v in ABSRET.items():
    temp = v.dropna()
    if len(temp) > 0:  # 30 entities don't have returns
        absret_stats['days_pos'][k] = len(temp[temp > 0]) / len(temp)
        absret_stats['days_neg'][k] = len(temp[temp < 0]) / len(temp)
        absret_stats['days_neut'][k] = len(temp[temp == 0]) / len(temp)

"""
Percentage of all days with absolute returns that are:
NEUTRAL
- median of percentage of days with NEUTRAL sentiment: 0.8 %
- mean of number of days with NEUTRAL sentiment: 1.02 %
- std of number of days with NEUTRAL sentiment: 0.91 %

POSITIVE:
- median of percentage of days with NEUTRAL sentiment: 50.54 %
- mean of number of days with NEUTRAL sentiment: 50.42 %
- std of number of days with NEUTRAL sentiment: 1.84 %

NEGATIVE:
- median of percentage of days with NEUTRAL sentiment: 48.55 %
- mean of number of days with NEUTRAL sentiment: 48.56 %
- std of number of days with NEUTRAL sentiment: 1.87 %
"""


alpha_stats = pd.DataFrame(index=ALPHA.columns,
                           columns=['days_pos', 'days_neg', 'days_neut'])
for k, v in ALPHA.items():
    temp = v.dropna()
    if len(temp) > 0:  # 30 entities don't have returns
        alpha_stats['days_pos'][k] = len(temp[temp > 0]) / len(temp)
        alpha_stats['days_neg'][k] = len(temp[temp < 0]) / len(temp)
        alpha_stats['days_neut'][k] = len(temp[temp == 0]) / len(temp)

"""
Percentage of all days with alphas that are:
NEUTRAL
- median of percentage of days with NEUTRAL sentiment: 0 %
- mean of number of days with NEUTRAL sentiment: 0 %
- std of number of days with NEUTRAL sentiment: 0 %

POSITIVE:
- median of percentage of days with POSITIVE sentiment: 49.84 %
- mean of number of days with POSITIVE sentiment: 49.75 %
- std of number of days with POSITIVE sentiment: 1.99 %

NEGATIVE:
- median of percentage of days with NEGATIVE sentiment: 50.16 %
- mean of number of days with NEGATIVE sentiment: 50.25 %
- std of number of days with NEGATIVE sentiment: 1.99 %
"""


def perc_of_days_with_matching_signs(entity_id, values):
    sentiments = RTRS_SENTIMENT_ENTITY[entity_id].dropna()
    values = values[sentiments.index]

    neg_values = values.apply(lambda x: x < 0)
    neg_sentiment = sentiments.apply(lambda x: x < 0)
    neg = neg_values & neg_sentiment

    pos_values = values.apply(lambda x: x > 0)
    pos_sentiment = sentiments.apply(lambda x: x > 0)
    pos = pos_values & pos_sentiment

    no_of_negative_days_matching = len(neg[neg is True])
    no_of_all_neg_sentiment_days = len(neg_sentiment[neg_sentiment is True])

    no_of_positive_days_matching = len(pos[pos is True])
    no_of_all_pos_sentiment_days = len(pos_sentiment[pos_sentiment is True])

    if no_of_all_neg_sentiment_days == 0:
        match_neg = 0
    else:
        match_neg = no_of_negative_days_matching / no_of_all_neg_sentiment_days

    if no_of_all_pos_sentiment_days == 0:
        match_pos = 0
    else:
        match_pos = no_of_positive_days_matching / no_of_all_pos_sentiment_days
    return match_pos, match_neg


sent_match_absret = pd.DataFrame(index=ABSRET.columns,
                                 columns=['matching_pos_%', 'matching_neg_%'])
for k, v in ABSRET.items():
    res = perc_of_days_with_matching_signs(k, v)
    sent_match_absret['matching_pos_%'][k] = res[0]
    sent_match_absret['matching_neg_%'][k] = res[1]

"""
Measures for number of days with absolute return matching sign of sentiment:

POSITIVE DAYS:
- mean: 50.8 %, i.e. 50.8 % of days with positive sentiment had positive abs.
                return on the same day (on average across all companies)
- median: 53.8 %
- std: 14.75 %

NEGATIVE DAYS:
- mean: 48.6 %, i.e. 48.6 % of days with negative sentiment had negative abs.
                return on the same day (on average across all companies)
- median: 51.6 %
- std: 14.6 %

Mean: mean of percentage of positive (negative) sentiment days that have
      positive (negative) absolute return on that day


If we discard entities that didn't have positive (negative) sentiment days at
all, and hence match percent is zero, we get a slight improvement in both
mean and median, and standard deviation is twice smaller

POSITIVE DAYS:
- mean: 54.0 %, i.e. 54.0 % of days with positive sentiment had positive abs.
                return on the same day (on average across all companies)
- median: 54.1 %
- std: 7.7 %

NEGATIVE DAYS:
- mean: 51.8 %, i.e. 51.8 % of days with negative sentiment had negative abs.
                return on the same day (on average across all companies)
- median: 51.9 %
- std: 7.7 %

"""


sent_match_alpha = pd.DataFrame(index=ALPHA.columns,
                                columns=['matching_pos_%', 'matching_neg_%'])
for k, v in ALPHA.items():
    res = perc_of_days_with_matching_signs(k, v)
    sent_match_alpha['matching_pos_%'][k] = res[0]
    sent_match_alpha['matching_neg_%'][k] = res[1]

"""
Measures for number of days with alpha matching the sign of sentiment:

POSITIVE DAYS:
- mean: 50.7 %, i.e. 50.7 % of days with positive sentiment had positive abs.
                return on the same day (on average across all companies)
- median: 53.8 %
- std: 14.6 %

NEGATIVE DAYS:
- mean: 50.3 %, i.e. 50.3 % of days with negative sentiment had negative abs.
                return on the same day (on average across all companies)
- median: 53.5 %
- std: 15.0 %

Mean: mean of percentage of positive (negative) sentiment days that have
      positive (negative) alpha on that day


If we discard entities that didn't have positive (negative) sentiment days at
all, and hence match percent is zero, we get a slight improvement in both
mean and median, and standard deviation is twice smaller

POSITIVE DAYS:
- mean: 53.7 %, i.e. 53.7 % of days with positive sentiment had positive abs.
                return on the same day (on average across all companies) after
                excluding entities that didn't have positive sentiment days at
                all
- median: 54.0 %
- std: 7.85 %

NEGATIVE DAYS:
- mean: 53.7 %, i.e. 53.7 % of days with negative sentiment had negative abs.
                return on the same day (on average across all companies) after
                excluding entities that didn't have negative sentiment days at
                all
- median: 53.8 %
- std: 7.8 %
"""


result = dict()
for entity_id, series in NEWS.items():
    days_with_news = len(series.dropna())
    days_with_sentiment_score = len(RTRS_SENTIMENT_ENTITY[entity_id].dropna())
    if days_with_news > 0:
        result[entity_id] = days_with_sentiment_score / days_with_news
"""
the difference between the number of days with sentiment measure and the number
of days with news:
- sometimes there is more days with sentiment measure than days with news,
  this is the case for 82 entities
- mean relation between days with sentiment score and news is quite high: 0.9
"""


ent_with_sent_by_day = RTRS_SENTIMENT_ENTITY.T.apply(lambda x: len(x.dropna()))
"""
###############################################################################
NUMBER OF ENTITIES WITH SENTIMENT SCORES (DAILY)
###############################################################################
Daily number of entities with sentiment scores
- 0.98 of days have less than 200 firms with sentiment score
- mean is 133.77, i.e. on average every day there are 133 entities with news
###############################################################################
"""

"""
###############################################################################
###############################################################################
Comparing daily aggregate level of sentiment with daily aggregate returns:
- 1519 days have negative aggregate sentiment
- 997 days have positive aggregate sentiment
###############################################################################
"""









