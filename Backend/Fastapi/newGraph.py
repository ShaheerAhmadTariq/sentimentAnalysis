from database import session,session1,session2,session3
from model import newsBrands, newsCompetitor, newsHashtag, redditBrands, redditCompetitor, redditHashtag, Base
from datetime import datetime, timedelta
from sqlalchemy import select, func
from collections import defaultdict
from typing import List, Dict, Any


def graph(brand: str, competitor: str, hashtag: str, day: int ):
    # return getDatafromtable(brand, newsBrands)
    days = day
    n_brands = getDatafromtable(brand, days, newsBrands)
    n_competitors = getDatafromtable(competitor, days, newsCompetitor)
    n_hashtag = getDatafromtable2(hashtag, days, newsHashtag)

    r_brands = getDatafromtable2(brand, days, redditBrands)
    # r_competitors = getDatafromtable(competitor, days, redditCompetitor)
    # r_hashtags = getDatafromtable(hashtag, days, redditHashtag)
    return "nothing"

def getDatafromtable(name: str,days : int,table: Base):
    rows = session.query(table).filter(table.name == name).all()
    return rows

def getDatafromtable2(name: str,days : int,table: Base):
    rows = session2.query(table).filter(table.name == name).all()
    return rows