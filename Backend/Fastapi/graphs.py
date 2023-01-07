from database import session
from model import newsBrands, newsCompetitor, newsHashtag, redditBrands, redditCompetitor, redditHashtag, Base
from datetime import datetime, timedelta
from sqlalchemy import select, func
from collections import defaultdict
from typing import List, Dict, Any
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
sia = SIA()
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
def getGraphs(brand: str, competitor: str, hashtag: str, days: int ):
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

    pos,neg,neutral = graph(result)
    return {"positive": pos, "negative": neg, "neutral":neutral}
    return n_brands, n_competitors, n_hashtag, r_brands, r_competitors, r_hashtags

def getNewsGraph(name: str, days : int, table: str):
    now = datetime.now()
    # # Calculate the date one month ago
    one_month_ago = now - timedelta(days=days)
    # query = session.query(newsBrands).filter(newsBrands.published_at >= one_month_ago, newsBrands.name == name)
    # # Execute the query and store the results in a list
    # results = query.all() 
    rows = session.query(table.content, func.date(table.published_at).label('published_at')).filter(table.published_at >= one_month_ago, table.name == name).all()
    # for row in rows:
    #     row.published_at = row.published_at.date()
        
    # return rows
    

    # Execute the query to get the rows from the newsBrands table
    # rows = session.query(newsBrands).all()

    # Create a defaultdict to store the content values as lists
    content_dict = defaultdict(list)

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