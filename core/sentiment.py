import pandas as pd

from blvresearch.core.utils import int2datetime
from blvresearch.core.sp500 import tick_to_ent_no_dupli
from blvresearch.core.utils import UniverseByEntityIdGenerator


PATH_TO_CSV = 'sp500news_cald.csv'

sentiment = pd.read_csv(PATH_TO_CSV)
sentiment = sentiment.drop(['date', 'sent_w', 'count', 'countrtrs'], axis=1)
sentiment['tdate'] = sentiment['tdate'].apply(int2datetime)

SENTIMENT_TICKER = pd.pivot_table(sentiment,
                                  values='sentrtrs',
                                  rows='tdate',
                                  cols='ticker')

SENTIMENT_ENTITY = SENTIMENT_TICKER.rename(columns=tick_to_ent_no_dupli)

changed = [c for c in SENTIMENT_ENTITY.columns if "-E" in c]

SENTIMENT_ENTITY = SENTIMENT_ENTITY[changed]

start = str(SENTIMENT_ENTITY.index[0]).split()[0]
end = str(SENTIMENT_ENTITY.index[-1]).split()[0]

UNIVERSE = UniverseByEntityIdGenerator(start, end).get(changed)

RTRS_SENTIMENT_ENTITY = SENTIMENT_ENTITY[list(UNIVERSE.keys())]
