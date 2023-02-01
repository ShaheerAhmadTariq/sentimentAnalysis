from database import session,session1,session2,session3, SessionLocal, session6, session10, SessionLocal
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
    session3 = SessionLocal()
    query = (
        session3.query(table.published_at, func.count(table.id).label("count").cast(Integer))
        .filter(table.name == name,table.published_at >= one_month_ago)
        .group_by(table.published_at)
        .all()
    )
    result_as_dict = [{row[0].strftime("%Y-%m-%d"):row[1]} for row in query]
    session3.close()
    return result_as_dict



def comparisonCountpie(brand: str, competitor: str, hashtag: str, day: int, p_id: int ):
    now = datetime.now()
    # # Calculate the date one month ago
    days = now - timedelta(days=day)
    newsCount =  getCount(newsBrands, brand, days)
    newsCount += getCount(newsCompetitor, competitor, days)
    newsCount += getCount(newsHashtag, hashtag, days)

    redditCount = getCount(redditBrands, brand, days)
    redditCount += getCount(redditCompetitor, competitor, days)
    redditCount += getCount(redditHashtag, hashtag, days)
    session6 = SessionLocal()
    result = session6.query(projectSentiments).filter(projectSentiments.project_id == p_id).first()
    # Total = result.p_sentiments['neutral'] + result.p_sentiments['negative'] + result.p_sentiments['positive']
    # Mentions = newsCount + redditCount
    Mentions = result.p_sentiments['positive'] + result.p_sentiments['negative'] + result.p_sentiments['neutral']
    # print(result.p_sentiments['neutral'])
    session6.close()
    return {"name": brand,"Total": Mentions, "Positive": result.p_sentiments['positive'], "Negative": result.p_sentiments['negative'], "Neutral": result.p_sentiments['neutral'],"NewsApi":newsCount, "Reddit": redditCount}
    return newsCount, redditCount
def getCount(table : Base, name: str, days: int):
    session17 = SessionLocal()
    count = (
    session17.query(table)
    .filter(table.name == name,table.published_at >= days)
    .count()
    )
    session17.close()
    return count

