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
# def getNewsGraph(rows: list): 
    # rows = session.query(table).all
    # return rows
    # rows = session.query(table.content, table.published_at).filter(table.published_at >= one_month_ago, table.name == name).all()
    rows = session5.query(table.content, func.date(table.published_at).label('published_at')).filter(table.published_at >= one_month_ago, table.name == name).all()
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
    # return contents