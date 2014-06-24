import pandas as pd

from memnews.core import NewsList


def get_absolute_co_occurrence(entity_id, data, freq='D'):
    other_entities = list(set(data.keys()) - set([entity_id]))
    entity_data = data[entity_id]
    result = pd.DataFrame(data=0,
                          index=entity_data.index,
                          columns=other_entities)
    for date, news_list in entity_data['news'].dropna().items():
        for news in news_list:
            common = list(set(news['entities']) &
                          set(other_entities))
            if common:
                result.loc[date][common] += 1
    return result.resample(freq, how=sum)


def get_relative_co_occurrence(entity_id, data, freq='D'):
    result = get_absolute_co_occurrence(entity_id, data, freq)
    news_count = _get_news_count(data, freq)
    result = _calculate_relative_occurrence(entity_id, result, news_count)
    return result


def _calculate_relative_occurrence(entity_id, abs_occ, news_counts):
    denom = _get_denominators(entity_id, news_counts)
    result = abs_occ.divide(denom)
    result.fillna(0, inplace=True)
    return result


def _get_denominators(entity_id, news_counts):
    to_add = news_counts[entity_id]
    result = news_counts.apply(func=lambda x: x + to_add, axis=0)
    return result.drop(entity_id, axis=1)


def _get_news_count(data, freq):
    def _get_count(x):
        return len(x) if isinstance(x, NewsList) else 0

    result = {k: v['news'].apply(_get_count) for k, v in data.items()}
    result = pd.DataFrame(result)
    result = result.resample(freq, how=sum)
    return result
