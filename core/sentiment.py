import pandas as pd

from blvresearch.core.utils import int2datetime
from blvresearch.core.sp500 import tick_to_ent_no_dupli
from blvresearch.core.utils import UniverseByEntityIdGenerator
from blvresearch.core.SP500output import ENTITIES_SP560


PATH_TO_CSV = 'sp500news_cald.csv'

sentiment = pd.read_csv(PATH_TO_CSV)

count = sentiment.drop(['date', 'sent_w', 'sentrtrs', 'count'], axis=1)
count['tdate'] = count['tdate'].apply(int2datetime)

sentiment = sentiment.drop(['date', 'sent_w', 'count', 'countrtrs'], axis=1)
sentiment['tdate'] = sentiment['tdate'].apply(int2datetime)

COUNT_TICKER = pd.pivot_table(count,
                              values='countrtrs',
                              rows='tdate',
                              cols='ticker')
SENTIMENT_TICKER = pd.pivot_table(sentiment,
                                  values='sentrtrs',
                                  rows='tdate',
                                  cols='ticker')

COUNT_ENTITY = COUNT_TICKER.rename(columns=tick_to_ent_no_dupli)
SENTIMENT_ENTITY = SENTIMENT_TICKER.rename(columns=tick_to_ent_no_dupli)

changed = [c for c in SENTIMENT_ENTITY.columns if "-E" in c]

COUNT_ENTITY = COUNT_ENTITY[changed]
SENTIMENT_ENTITY = SENTIMENT_ENTITY[changed]

start = str(SENTIMENT_ENTITY.index[0]).split()[0]
end = str(SENTIMENT_ENTITY.index[-1]).split()[0]

UNIVERSE = UniverseByEntityIdGenerator(start, end).get(changed)

RTRS_SENTIMENT_ENTITY = SENTIMENT_ENTITY[ENTITIES_SP560]
RTRS_COUNT_ENTITY = COUNT_ENTITY[ENTITIES_SP560]
