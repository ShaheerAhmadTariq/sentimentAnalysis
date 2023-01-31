from database import session,session1,session2,session3, SessionLocal, session6
from model import newsBrands, newsCompetitor, newsHashtag, redditBrands, redditCompetitor, redditHashtag, Base, projectSentiments
from datetime import datetime, timedelta
from sqlalchemy import select, func, Integer
from collections import defaultdict
from typing import List, Dict, Any


def joinDict(first: List[Dict[str, Any]], second: List[Dict[str, Any]]):
    for d in second:
        for key, value in d.items():
            found = False
            for dict_ in first:
                if key in dict_:
                    dict_[key] += value
                    found = True
                    break
            if not found:
                first.append({key: value})
    return first



def comparisonLineChart(brand: str, competitor: str, hashtag: str, day: int ):
    now = datetime.now()
    days = now - timedelta(days=day)
    n_brands = getNewsGraph(brand, days, newsBrands)
    n_competitors = getNewsGraph(competitor, days, newsCompetitor)
    n_hashtag = getNewsGraph(hashtag, days, newsHashtag)

    r_brands = getNewsGraph(brand, days, redditBrands)
    r_competitors = getNewsGraph(competitor, days, redditCompetitor)
    r_hashtags = getNewsGraph(hashtag, days, redditHashtag)

    result = joinDict(n_brands,n_competitors)
    result = joinDict(result, n_hashtag)
    result = joinDict(result, r_brands)
    result = joinDict(result, r_competitors)
    result = joinDict(result, r_hashtags)

    return result

def getNewsGraph(name: str, one_month_ago : int, table: str):
    query = (
        session3.query(table.published_at, func.count(table.id).label("count").cast(Integer))
        .filter(table.name == name,table.published_at >= one_month_ago)
        .group_by(table.published_at)
        .all()
    )
    result_as_dict = [{row[0].strftime("%Y-%m-%d"):row[1]} for row in query]
    return result_as_dict

# def getNewsGraph(name: str, one_month_ago : int, table: str):
#     query = (
#         session.query(table.published_at, func.count(table.id))
#         .filter(table.published_at >= one_month_ago)
#         .group_by(table.published_at)
#         .all()
#     )
#     result_as_dict = [{"published_at": row[0].strftime("%Y-%m-%d"), "count": row[1]} for row in query]
#     return result_as_dict
    # rows = session.query(table.content, func.date(table.published_at).label('published_at')).filter(table.published_at >= one_month_ago, table.name == name).all()


    # content_dict = defaultdict(list)
    # for row in rows:
    #     content_dict[row.published_at].append(row.content)

    # return sentiment_dict

def comparisonCountpie(brand: str, competitor: str, hashtag: str, day: int, p_id: int ):
    newsCount =  getCount(newsBrands, brand)
    newsCount += getCount(newsCompetitor, competitor)
    newsCount += getCount(newsHashtag, hashtag)

    redditCount = getCount(redditBrands, brand)
    redditCount += getCount(redditCompetitor, competitor)
    redditCount += getCount(redditHashtag, hashtag)
    session6 = SessionLocal()
    result = session6.query(projectSentiments).filter(projectSentiments.project_id == p_id).first()
    # Total = result.p_sentiments['neutral'] + result.p_sentiments['negative'] + result.p_sentiments['positive']
    # Mentions = newsCount + redditCount
    Mentions = result.p_sentiments['positive'] + result.p_sentiments['negative']
    # print(result.p_sentiments['neutral'])

    return {"name": brand,"Total": Mentions, "Positive": result.p_sentiments['positive'], "Negative": result.p_sentiments['negative'],"NewsApi":newsCount, "Reddit": redditCount}
    return newsCount, redditCount
def getCount(table : Base, name: str):
    count = (
    session6.query(table)
    .filter(table.name == name)
    .count()
    )
    return count

def handleExceptiongetCount():
    return {"project01":{"name":"apple","Total":416,"Positive":243,"Negative":66,"NewsApi":70,"Reddit":346},"project02":{"name":"pepsi","Total":42,"Positive":22,"Negative":12,"NewsApi":37,"Reddit":5}}

def handleExceptionLineChart():
    return {"project01":[{"2022-12-29":20},{"2022-12-30":16},{"2023-01-02":16},{"2023-01-03":2},{"2023-01-04":4},{"2023-01-05":14},{"2023-01-06":16},{"2023-01-08":2},{"2023-01-09":6},{"2023-01-10":16},{"2023-01-11":28},{"2023-01-12":18},{"2023-01-13":28},{"2023-01-14":32},{"2023-01-15":9},{"2023-01-17":30},{"2023-01-18":30},{"2023-01-19":18},{"2023-01-20":16},{"2023-01-21":22},{"2023-01-23":8},{"2023-01-24":26},{"2023-01-25":16}],"project02":[{"2022-12-29":30},{"2022-12-30":6},{"2023-01-02":6},{"2023-01-03":12},{"2023-01-04":24},{"2023-01-05":24},{"2023-01-06":6},{"2023-01-08":12},{"2023-01-09":6},{"2023-01-10":6},{"2023-01-11":48},{"2023-01-12":48},{"2023-01-13":18},{"2023-01-14":12},{"2023-01-15":12},{"2023-01-17":30},{"2023-01-18":30},{"2023-01-19":18},{"2023-01-20":6},{"2023-01-21":12},{"2023-01-23":18},{"2023-01-24":6},{"2023-01-25":6}]}

def handleExceptionPieChart():
    return {"project01":{"name":"apple","Total":416,"Positive":243,"Negative":66,"NewsApi":70,"Reddit":346}}