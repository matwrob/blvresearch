import pandas as pd

from memnews.core import NewsList


def get_coocc_with_other_entities(entity_id, data, freq='B'):
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


def get_relative_coocc_with_other_entities(entity_id, data, freq='D'):
    result = get_coocc_with_other_entities(entity_id, data, freq)
    news_count = _get_news_count(data, freq)
    result = _calculate_relative_occurrence(entity_id, result, news_count)
    return result


def _calculate_relative_occurrence(entity_id, abs_occ, news_counts):
    denom = _get_denominators(entity_id, abs_occ, news_counts)
    result = abs_occ.divide(denom)
    result.fillna(0, inplace=True)
    return result


def _get_denominators(entity_id, abs_occ, news_counts):
    """denominator for relative score should be the sum of all unique news
    for both entities, therefore for each other entity we take its news count,
    add news count of entity in question and subtract the count of shared news,
    because otherwise they would be counted twice

    """
    to_add = abs_occ.mul(-1).add(news_counts[entity_id], axis=0)
    result = news_counts.add(to_add)
    return result.drop(entity_id, axis=1)


def _get_news_count(data, freq):
    def _get_count(x):
        return len(x) if isinstance(x, NewsList) else 0

    result = {k: v['news'].apply(_get_count) for k, v in data.items()}
    result = pd.DataFrame(result)
    result = result.resample(freq, how=sum)
    return result
