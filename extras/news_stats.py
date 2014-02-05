from collections import Counter
from itertools import chain
import pandas as pd

from blvresearch.utils import db, start, end


START_YEAR = 2002
END_YEAR = 2013


news_entities = {k: db.get_news_entities(start(k), end(k))
                 for k in range(START_YEAR, END_YEAR + 1)}

total_news_published = {k: len(v) for k, v in news_entities.items()}

news_per_entity = {k: pd.Series(Counter(chain.from_iterable(v)))
                   for k, v in news_entities.items()}

no_of_entities_covered = {k: len(v) for k, v in news_per_entity.items()}

descr_stats = pd.DataFrame(index=range(START_YEAR, END_YEAR + 1),
                           columns=["total_news_published",
                                    "no_of_entities_covered",
                                    "per_entity_mean",
                                    "per_entity_std",
                                    "per_entity_median",
                                    "per_entity_max",
                                    "per_entity_min",
                                    "entities_with_>=_25_news",
                                    "entities_with_>=_50_news",
                                    "entities_with_>=_100_news",
                                    "entities_with_>=_150_news"])
descr_stats["total_news_published"] = pd.Series(total_news_published)
descr_stats["no_of_entities_covered"] = pd.Series(no_of_entities_covered)
descr_stats["per_entity_mean"] = pd.Series(
    {k: v.mean() for k, v in news_per_entity.items()}
)
descr_stats["per_entity_std"] = pd.Series(
    {k: v.std() for k, v in news_per_entity.items()}
)
descr_stats["per_entity_median"] = pd.Series(
    {k: v.median() for k, v in news_per_entity.items()}
)
descr_stats["per_entity_max"] = pd.Series(
    {k: v.max() for k, v in news_per_entity.items()}
)
descr_stats["per_entity_min"] = pd.Series(
    {k: v.min() for k, v in news_per_entity.items()}
)
descr_stats["entities_with_>=_25_news"] = pd.Series(
    {k: len(v[v >= 25]) for k, v in news_per_entity.items()}
)
descr_stats["entities_with_>=_50_news"] = pd.Series(
    {k: len(v[v >= 50]) for k, v in news_per_entity.items()}
)
descr_stats["entities_with_>=_100_news"] = pd.Series(
    {k: len(v[v >= 100]) for k, v in news_per_entity.items()}
)
descr_stats["entities_with_>=_150_news"] = pd.Series(
    {k: len(v[v >= 150]) for k, v in news_per_entity.items()}
)
