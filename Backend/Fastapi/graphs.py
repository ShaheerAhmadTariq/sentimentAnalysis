from database import session,session1,session2,session3 ,Base

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
    # try:
    #     # n_brands = getNewsGraph(brand, days, newsBrands)
    #     row = session.query(newsBrands.content, func.date(newsBrands.published_at).label('published_at')).filter(newsBrands.published_at >= days, newsBrands.name == brand).all()
    #     n_brands = getNewsGraph(row)
    #     # session.expire_all()
    #     row2 = session1.query(newsCompetitor.content, func.date(newsCompetitor.published_at).label('published_at')).filter(newsCompetitor.published_at >= days, newsCompetitor.name == competitor).all()
    #     n_competitors = getNewsGraph(row2)
    #     # session.expire_all()
    #     row3 = session.query(newsHashtag.content, func.date(newsHashtag.published_at).label('published_at')).filter(newsHashtag.published_at >= days, newsHashtag.name == hashtag).all()
    #     n_hashtag = getNewsGraph(row3)
    #     # session.expire_all()
    #     row4 = session2.query(redditBrands.content, func.date(redditBrands.published_at).label('published_at')).filter(redditBrands.published_at >= days, redditBrands.name == brand).all()
    #     r_brands = getNewsGraph(row4)
    #     # session.expire_all()
    #     row5 = session3.query(redditCompetitor.content, func.date(redditCompetitor.published_at).label('published_at')).filter(redditCompetitor.published_at >= days, redditCompetitor.name == competitor).all()
    #     r_competitors = getNewsGraph(row5)
    #     # session.expire_all()
    #     row6 = session.query(redditHashtag.content, func.date(redditHashtag.published_at).label('published_at')).filter(redditHashtag.published_at >= days, redditHashtag.name == hashtag).all()
    #     r_hashtags = getNewsGraph(row6)
    #     session.expire_all()
    # except:
    #     return "err"
    # try:
    n_brands = getNewsGraph(brand, days, newsBrands)
    n_competitors = getNewsGraph(competitor, days, newsCompetitor)
    n_hashtag = getNewsGraph2(hashtag, days, newsHashtag)

    r_brands = getNewsGraph2(brand, days, redditBrands)
    r_competitors = getNewsGraph3(competitor, days, redditCompetitor)
    r_hashtags = getNewsGraph3(hashtag, days, redditHashtag)
        # n_brands = getNewsGraph(brand, days, newsBrands, session)
        # n_competitors = getNewsGraph(competitor, days, newsCompetitor, session)
        # n_hashtag = getNewsGraph(hashtag, days, newsHashtag, session)

        # r_brands = getNewsGraph(brand, days, redditBrands, session)
        # r_competitors = getNewsGraph(competitor, days, redditCompetitor, session)
        # r_hashtags = getNewsGraph(hashtag, days, redditHashtag, session)
    # except:
        # return {'err':'while running'}
    # session.close()
    # session1.close()
    # session2.close()
    result = joinDict(n_brands,n_competitors)
    result = joinDict(result, n_hashtag)
    result = joinDict(result, r_brands)
    result = joinDict(result, r_competitors)
    result = joinDict(result, r_hashtags)
    # except:
        # return "err"
    pos,neg,neutral = graph(result)
    # pos,neg,neutral = (0,0,0)
    
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
    rows = session1.query(table.content, func.date(table.published_at).label('published_at')).filter(table.published_at >= one_month_ago, table.name == name).all()
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
    rows = session2.query(table.content, func.date(table.published_at).label('published_at')).filter(table.published_at >= one_month_ago, table.name == name).all()
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