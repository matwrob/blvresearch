from collections import defaultdict
from itertools import chain
import datetime as dt
import pandas as pd

from blvresearch.concat.analysts.reuters.researchline import (
    ResearchLine, is_research_line
)
from blvresearch.concat.analysts.reuters.normalizer import (
    normalize_line
)
from memnews.entity_security_transl import (
    ric_entity_transl
)
from concat_overlord.dbpools import BLVPRICES_READ, FSDB
from blvprices.universe import Security
from blvutils.sql import sql_values
from memnews.dbpools import NEWSDB


TRANSL = ric_entity_transl()


def get_analysts_recommendations_for_entities(entities, start_date, end_date):
    news_items = get_reuters_research_news(entities, start_date, end_date)
    news_items = [n for n in news_items if n['body'].strip()]
    return get_analysts_recommendations_from_news_items(news_items)


def get_analysts_recommendations_from_news_items(list_of_news_items):
    news_items = [n for n in list_of_news_items if n['body'].strip()]
    entities = _get_all_entities_from_news_items(news_items)
    result = prepare_result_container(entities)
    for news in news_items:
        research_lines = _get_research_lines(news)
        for line in research_lines:
            e_id = line.analyzed_entity
            if e_id and e_id in result.keys():
                index = result[e_id].index
                date = _determine_proper_date(news['story_time'], index)
                if line not in result[e_id][date]:
                    result[e_id][date].append(line)
    return result


def _determine_proper_date(datetime, date_index):
    this_time = pd.Timestamp(datetime)
    this_time = this_time.tz_localize('UTC')
    older_dates = [i for i in date_index if i > this_time]
    older_dates = pd.DatetimeIndex(older_dates)
    return older_dates.min()


def _get_research_lines(reuters_news):
    all_lines = reuters_news['body'].split('\n')
    tmp = list()
    for line in all_lines:
        norm_line = normalize_line(line)
        if is_research_line(norm_line):
            rl = ResearchLine(norm_line)
            rl.find_info()
            if rl.analyzed_entity is None:
                rl = _add_entity_info(rl, reuters_news)
            if rl not in tmp:
                tmp.append(rl)
    return tmp


def _add_entity_info(research_line, news):
    entities = [TRANSL.flipget(r) for r in news['rics']]
    entities = list(set(entities))
    if len(entities) == 1:
        research_line.analyzed_entity = entities[0]
    return research_line


def prepare_result_container(entities):  # pragma: no cover
    fs_perm_sec_ids = _get_fs_perm_sec_ids(entities)
    securities = _get_security_objects(list(fs_perm_sec_ids.values()))
    fs_indices = _get_factset_indices(list(fs_perm_sec_ids.values()))
    result = dict()
    for e_id, sec in securities.items():
        fs_index = fs_indices[sec.fs_perm_sec_id]
        correct_index = _add_correct_time(sec, fs_index)
        result[e_id] = pd.Series({i: list() for i in correct_index})
    return result


def get_reuters_research_news(entities, start, end):  # pragma: no cover
    rics = list(chain.from_iterable([TRANSL.get(e) for e in entities
                                     if TRANSL.get(e)]))
    q = """SELECT story_time, body, rics
           FROM reuters_item
           WHERE story_time >= %s
           AND story_time <= %s
           AND language = 'en'
           AND topics && %s
           AND rics && %s
        """
    conn = NEWSDB.connect()
    res = conn.execute(q, (start, end, ['RCH'], rics))
    conn.close()
    result = list()
    for r in res:
        result.append({'story_time': r[0],
                       'body': r[1],
                       'rics': r[2]})
    return result


def _get_fs_perm_sec_ids(entities):  # pragma: no cover
    q = """SELECT factset_entity_id, fs_perm_sec_id
           FROM universe_item
           WHERE factset_entity_id = ANY({0})
        """.format(sql_values(entities))
    res = BLVPRICES_READ.execute(q, entities)
    result = dict()
    for t in res.fetchall():
        if t[0] not in result.keys():
            result[t[0]] = t[1]
        if t[1] != result[t[0]]:
            print('two different fs_perm_sec_ids?????')
    return result


def _get_security_objects(fs_perm_sec_ids):  # pragma: no cover
    q = """SELECT * FROM universe_item
           WHERE universe_id = 'RESEARCH_2014'
           AND fs_perm_sec_id = ANY({0})
        """.format(sql_values(fs_perm_sec_ids))
    res = BLVPRICES_READ.execute(q, fs_perm_sec_ids)
    res = [Security(r) for r in res.fetchall()]
    return {sec.factset_entity_id: sec for sec in res}


def _get_factset_indices(fs_perm_sec_ids):  # pragma: no cover
    "for c.a. 1100 ids getting data from db takes around 3-4 minutes"
    q = """SELECT date, fs_perm_sec_id
           FROM fp_basic_bd
           WHERE fs_perm_sec_id = ANY({0})
        """.format(sql_values(fs_perm_sec_ids))
    res = FSDB.execute(q, fs_perm_sec_ids)
    result = defaultdict(list)
    for t in res.fetchall():
        result[t[1]].append(t[0])
    return {k: pd.DatetimeIndex(v) for k, v in result.items()}


def _add_correct_time(security, date_index):  # pragma: no cover
    time = security.exchange['close'].split(':')
    add_time = dt.timedelta(hours=int(time[0]), minutes=int(time[1]))
    new_index = date_index + add_time
    new_index = new_index.tz_localize(security.exchange['zone'])
    new_index = new_index.tz_convert('UTC')
    return new_index


def _get_all_entities_from_news_items(list_of_news_items):  # pragma: no cover
    rics = [v['rics'] for v in list_of_news_items]
    all_rics = list(set(chain.from_iterable(rics)))
    result = [TRANSL.flipget(r) for r in all_rics]
    return [r for r in result if r]
