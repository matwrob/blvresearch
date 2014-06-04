from memnews.core import NewsList


def alert_news(news_list):
    ids = [n["id"] for n in news_list if n["type"] == "alert"]
    return NewsList(ids)


def long_feature_news(news_list):
    ids = [n["id"] for n in news_list if n["type"] == "long_feature"]
    return NewsList(ids)


def feature_news(news_list):
    ids = [n["id"] for n in news_list if "feature" in n["type"]]
    return NewsList(ids)
