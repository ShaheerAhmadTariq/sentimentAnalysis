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
    new_dict = {**first, **second}
    for key in new_dict.keys():
        if key in first:
            value = first[key]
            new_value = new_dict[key]
            b,c,h = new_value
            b += value[0]
            c += value[1]
            h += value[2]
            new_dict[key] = [b,c,h]
    return new_dict
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
    n_brands = getNewsGraph(brand, days, newsBrands)
    n_competitors = getNewsGraph(competitor, days, newsCompetitor)
    n_hashtag = getNewsGraph2(hashtag, days, newsHashtag)

    r_brands = getNewsGraph2(brand, days, redditBrands)
    r_competitors = getNewsGraph3(competitor, days, redditCompetitor)
    r_hashtags = getNewsGraph3(hashtag, days, redditHashtag)
    result = joinDict(n_brands,n_competitors)
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
    return {"multiGraph":{"positive":{"2023-01-14":8,"2023-01-12":16,"2023-01-19":48,"2023-01-05":32,"2023-01-11":48,"2023-01-18":96,"2023-01-25":108,"2023-01-17":112,"2023-01-13":0,"2022-12-29":32,"2023-01-03":32,"2023-01-04":80,"2023-01-08":32,"2022-12-30":32,"2023-01-02":18,"2023-01-09":0,"2023-01-15":32,"2023-01-23":100,"2023-01-07":32,"2023-01-16":16,"2023-01-24":180,"2023-01-21":32,"2023-01-20":16,"2023-01-01":0,"2023-01-26":54,"2023-01-27":68,"2023-01-06":0},"negative":{"2023-01-14":16,"2023-01-12":0,"2023-01-19":0,"2023-01-05":0,"2023-01-11":0,"2023-01-18":0,"2023-01-25":16,"2023-01-17":0,"2023-01-13":0,"2022-12-29":16,"2023-01-03":16,"2023-01-04":32,"2023-01-08":32,"2022-12-30":0,"2023-01-02":0,"2023-01-09":16,"2023-01-15":0,"2023-01-23":30,"2023-01-07":16,"2023-01-16":0,"2023-01-24":44,"2023-01-21":0,"2023-01-20":0,"2023-01-01":0,"2023-01-26":16,"2023-01-27":16,"2023-01-06":2},"neutral":{"2023-01-14":0,"2023-01-12":64,"2023-01-19":16,"2023-01-05":32,"2023-01-11":48,"2023-01-18":32,"2023-01-25":32,"2023-01-17":16,"2023-01-13":32,"2022-12-29":0,"2023-01-03":16,"2023-01-04":32,"2023-01-08":0,"2022-12-30":0,"2023-01-02":2,"2023-01-09":8,"2023-01-15":0,"2023-01-23":44,"2023-01-07":0,"2023-01-16":0,"2023-01-24":100,"2023-01-21":0,"2023-01-20":0,"2023-01-01":8,"2023-01-26":24,"2023-01-27":30,"2023-01-06":0}},"singleGraph":{"result":{"2023-01-14":24,"2023-01-12":80,"2023-01-19":64,"2023-01-05":64,"2023-01-11":96,"2023-01-18":128,"2023-01-25":156,"2023-01-17":128,"2023-01-13":32,"2022-12-29":48,"2023-01-03":64,"2023-01-04":144,"2023-01-08":64,"2022-12-30":32,"2023-01-02":20,"2023-01-09":24,"2023-01-15":32,"2023-01-23":174,"2023-01-07":48,"2023-01-16":16,"2023-01-24":324,"2023-01-21":32,"2023-01-20":16,"2023-01-01":8,"2023-01-26":94,"2023-01-27":114,"2023-01-06":2}}}