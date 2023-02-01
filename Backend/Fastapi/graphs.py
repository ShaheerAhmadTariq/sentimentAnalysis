from database import session,session1,session2,session3,session5,session6 ,Base

from model import newsBrands, newsCompetitor, newsHashtag, redditBrands, redditCompetitor, redditHashtag, Base
from datetime import datetime, timedelta
from sqlalchemy import select, func
from collections import defaultdict
from typing import List, Dict, Any
# import nltk
# nltk.download('vader_lexicon')
# from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
# sia = SIA()
from sentiment import sia

def getSingleLineChart(input: dict[str,Any]):
    pos = input['positive']
    neg = input['negative']
    neutral = input['neutral']
    finalDict= {}
    for keys in pos.keys():
        finalDict[keys] = pos[keys] + neg[keys] + neutral[keys]
    return {"result": finalDict}



def joinDict(first: dict[str, Any],second: dict[str, Any]):
    result = {}
    for key,val in first.items():
        if key in second.keys():
            l1,l2,l3 = second[key]
            result[key] = [val[0]+l1, val[1]+l2, val[2]+l3]
        else:
            result[key] = val
    for key,val in second.items():
        if key not in result.keys():
            result[key] = val
    return result

def graph(result):
    pos = {}
    neg = {}
    neutral = {}
    for key in result.keys():
        p,n,neu = result[key]
        pos[key] = p
        neg[key] = n
        neutral[key] = neu
    return pos,neg,neutral
# pos,neg,neu = graph(result)
def getGraphs(brand: str, competitor: str, hashtag: str, day: int ):
    now = datetime.now()
    # # Calculate the date one month ago
    days = now - timedelta(days=day)
    # days = 1000
    n_brands = getNewsGraph(brand, days, newsBrands)
    n_competitors = getNewsGraph(competitor, days, newsCompetitor)
    n_hashtag = getNewsGraph2(hashtag, days, newsHashtag)

    r_brands = getNewsGraph2(brand, days, redditBrands)
    r_competitors = getNewsGraph3(competitor, days, redditCompetitor)
    r_hashtags = getNewsGraph3(hashtag, days, redditHashtag)
    
    result = joinDict(n_competitors,n_brands)

    result = joinDict(result, n_hashtag)
    result = joinDict(result, r_brands)
    result = joinDict(result, r_competitors)
    result = joinDict(result, r_hashtags)
    pos,neg,neutral = graph(result)
    
    return {"positive": pos, "negative": neg, "neutral": neutral}
    

def getNewsGraph(name: str, one_month_ago : int, table: str): 
# def getNewsGraph(rows: list): 
    # rows = session.query(table).all
    # return rows
    # rows = session.query(table.content, table.published_at).filter(table.published_at >= one_month_ago, table.name == name).all()
    rows = session3.query(table.content, func.date(table.published_at).label('published_at')).filter(table.published_at >= one_month_ago, table.name == name).all()
    
    # rows = session.query(table.content, table.published_at).filter(table.published_at >= one_month_ago, table.name == name).all()
    # rows = session.query(table).all
    # stmt = select([table.content, func.date(table.published_at).label('published_at')]).where(table.published_at >= one_month_ago)
    # rows = session.execute(stmt).fetchall()

    content_dict = defaultdict(list)
    # print(rows)
    # Iterate through the rows and add the content values to the appropriate key in the content_dict
    for row in rows:
        content_dict[row.published_at].append(row.content)
    sentiment_dict = {}
    for key in content_dict.keys():
        sentiment = getSentiment(content_dict[key])
        sentiment_dict[key] = sentiment
    return sentiment_dict

def getNewsGraph2(name: str, one_month_ago : int, table: str): 
# def getNewsGraph(rows: list): 
    # rows = session.query(table).all
    # return rows
    # rows = session.query(table.content, table.published_at).filter(table.published_at >= one_month_ago, table.name == name).all()
    rows = session6.query(table.content, func.date(table.published_at).label('published_at')).filter(table.published_at >= one_month_ago, table.name == name).all()
    # rows = session.query(table.content, table.published_at).filter(table.published_at >= one_month_ago, table.name == name).all()
    # rows = session.query(table).all
    # stmt = select([table.content, func.date(table.published_at).label('published_at')]).where(table.published_at >= one_month_ago)
    # rows = session.execute(stmt).fetchall()

    content_dict = defaultdict(list)
    # print(rows)
    # Iterate through the rows and add the content values to the appropriate key in the content_dict
    for row in rows:
        content_dict[row.published_at].append(row.content)
    sentiment_dict = {}
    for key in content_dict.keys():
        sentiment = getSentiment(content_dict[key])
        sentiment_dict[key] = sentiment
    return sentiment_dict

def getNewsGraph3(name: str, one_month_ago : int, table: str): 
    rows = session5.query(table.content, func.date(table.published_at).label('published_at')).filter(table.published_at >= one_month_ago, table.name == name).all()
    

    content_dict = defaultdict(list)
    for row in rows:
        content_dict[row.published_at].append(row.content)
    sentiment_dict = {}
    for key in content_dict.keys():
        sentiment = getSentiment(content_dict[key])
        sentiment_dict[key] = sentiment
    return sentiment_dict

def getSentiment(content: list):
    # contents = []
    positive = 0
    negative = 0
    neutral = 0
    # print(content)
    for data in content:
        # contents.append(data)
        
        
        result = sia.polarity_scores(data)
        # print(result)
        if result['compound'] >= 0.05 :
                positive += 1
                # content.append(positive)
        elif result['compound'] <= - 0.05 :
            negative += 1
            # content.append(negative)
        else :
            neutral += 1

    return positive,negative,neutral

def handleExceptionSentimentGraph():
    return {"multiGraph":{"positive":{"2023-01-02":32,"2023-01-03":32,"2023-01-04":40,"2023-01-05":24,"2023-01-06":0,"2023-01-07":64,"2023-01-08":8,"2023-01-09":24,"2023-01-10":24,"2023-01-11":40,"2023-01-12":32,"2023-01-13":16,"2023-01-14":8,"2023-01-15":8,"2023-01-16":16,"2023-01-17":104,"2023-01-18":64,"2023-01-19":32,"2023-01-20":32,"2023-01-21":96,"2023-01-22":8,"2023-01-23":49,"2023-01-24":49,"2023-01-25":27,"2023-01-26":6,"2023-01-27":6,"2023-01-28":11,"2023-01-29":4,"2023-01-30":75,"2023-01-31":37},"negative":{"2023-01-02":0,"2023-01-03":24,"2023-01-04":48,"2023-01-05":0,"2023-01-06":0,"2023-01-07":32,"2023-01-08":8,"2023-01-09":8,"2023-01-10":0,"2023-01-11":24,"2023-01-12":32,"2023-01-13":0,"2023-01-14":8,"2023-01-15":8,"2023-01-16":0,"2023-01-17":16,"2023-01-18":8,"2023-01-19":0,"2023-01-20":0,"2023-01-21":0,"2023-01-22":0,"2023-01-23":15,"2023-01-24":11,"2023-01-25":4,"2023-01-26":1,"2023-01-27":2,"2023-01-28":0,"2023-01-29":1,"2023-01-30":25,"2023-01-31":22},"neutral":{"2023-01-02":0,"2023-01-03":32,"2023-01-04":64,"2023-01-05":16,"2023-01-06":32,"2023-01-07":0,"2023-01-08":0,"2023-01-09":0,"2023-01-10":24,"2023-01-11":32,"2023-01-12":40,"2023-01-13":8,"2023-01-14":0,"2023-01-15":0,"2023-01-16":8,"2023-01-17":8,"2023-01-18":48,"2023-01-19":16,"2023-01-20":8,"2023-01-21":0,"2023-01-22":0,"2023-01-23":30,"2023-01-24":27,"2023-01-25":8,"2023-01-26":7,"2023-01-27":6,"2023-01-28":9,"2023-01-29":5,"2023-01-30":30,"2023-01-31":30}},"singleGraph":{"result":{"2023-01-02":32,"2023-01-03":88,"2023-01-04":152,"2023-01-05":40,"2023-01-06":32,"2023-01-07":96,"2023-01-08":16,"2023-01-09":32,"2023-01-10":48,"2023-01-11":96,"2023-01-12":104,"2023-01-13":24,"2023-01-14":16,"2023-01-15":16,"2023-01-16":24,"2023-01-17":128,"2023-01-18":120,"2023-01-19":48,"2023-01-20":40,"2023-01-21":96,"2023-01-22":8,"2023-01-23":94,"2023-01-24":87,"2023-01-25":39,"2023-01-26":14,"2023-01-27":14,"2023-01-28":20,"2023-01-29":10,"2023-01-30":130,"2023-01-31":89}}}