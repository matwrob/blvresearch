import re


def get_analysts_data(news):
    lines = _get_analysts_lines(news['body'])
    result = dict()
    for line in lines:
        researched_entity = _get_researched_entity(line)
        tmp = dict()
        tmp['action'] = _get_action(line)
        tmp['analyst'] = _get_analyst(line)
        tmp['rating'] = _get_rating(line)
        result[researched_entity] = tmp
    return result


def _get_action(string):
    if re.search(r'cut[s]', string):
        return 'cut'
    if re.search(r'raise(s|d)', string):
        return 'raise'
    return ''


def _get_analyst(string):
    string = string.split(':')[1]
    result = [s for s in string.split() if s[0].isupper()]
    return " ".join(result)


def _get_rating(string):
    RATINGS = ["underweight", "overweight", "equal weight", "equal-weight",
               "buy", "hold", "sell", "outperform", "neutral", "underperform",
               "accumulate", "reduce"]
    if 'rating' in string:
        split = string.split('rating')
        if split[1].strip() in RATINGS:
            return split[1].strip()
        elif split[0].split().strip()[-1] in RATINGS:
            return split[0].split().strip()[-1]
        else:
            return ''


def _get_researched_entity(string):
    string = string.lstrip('*')
    return string.split(':')[0].strip()


def _get_analysts_lines(string):
    all_lines = string.split('\n')
    return [l for l in all_lines if l.startswith('*')]



analysts_news = get_reuters_analysts_news(news_list)


def get_reuters_analysts_news(news_list):
    news_ids = [n['id'].split('-')[1] for n in news_list
                if n['provider'] == 'reuters']
    news_topics = get_news_topics(news_ids, NEWSDB)
    return [n for n in news_list if "RCH" in news_topics[n['id']]]





def has_key_phrases(news):
    ch, nb, b = news['clean_headline'], news['normalized_body'], news['body']
    head_price_target = 'price target' in ch or 'target price' in ch
    body_price_target = 'price target' in nb or 'target price' in nb
    if head_price_target:
        return True
    if body_price_target:
        return True
    return False


RATINGS_UNION = "|".join(RATINGS)
PRICE = r"[0-9]+(\,|\.)*[0-9]*"
FROM_TO_1 = r"(to|from).{5}" + PRICE + r"(from|to).{5}" + PRICE
FROM_TO_2 = (r"(to|from).{2}" + "(%s)" % RATINGS_UNION +
             r"(to|from).{2}" + "(%s)" % RATINGS_UNION)
