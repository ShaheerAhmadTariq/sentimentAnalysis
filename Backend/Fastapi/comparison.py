from database import session,session1,session2,session3, SessionLocal
from model import newsBrands, newsCompetitor, newsHashtag, redditBrands, redditCompetitor, redditHashtag, Base, projectSentiments
from datetime import datetime, timedelta
from sqlalchemy import select, func
from collections import defaultdict
from typing import List, Dict, Any

def comparisonCountpie(brand: str, competitor: str, hashtag: str, day: int ):
    newsCount =  getCount(newsBrands, brand)
    newsCount += getCount(newsCompetitor, competitor)
    newsCount += getCount(newsHashtag, hashtag)

    redditCount = getCount(redditBrands, brand)
    redditCount += getCount(redditCompetitor, competitor)
    redditCount += getCount(redditHashtag, hashtag)
    session6 = SessionLocal()
    result = session6.query(projectSentiments).filter(projectSentiments.project_id == 1).first()
    # Total = result.p_sentiments['neutral'] + result.p_sentiments['negative'] + result.p_sentiments['positive']
    Mentions = newsCount + redditCount
    # print(result.p_sentiments['neutral'])

    return {"Total": Mentions, "Positive": result.p_sentiments['positive'], "Negative": result.p_sentiments['negative'],"news":newsCount, "reddit": redditCount}
    return newsCount, redditCount
def getCount(table : Base, name: str):
    count = (
    session.query(table)
    .filter(table.name == name)
    .count()
    )
    return count
