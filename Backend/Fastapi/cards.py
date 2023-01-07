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

def getCards(brand: str, competitor: str, hashtag: str, days: int ):
    positive = []
    negative = []
    neutral = []
    pos,neg,neu = getNewsCard(brand, days, newsBrands)
    positive.extend(pos)
    negative.extend(neg)
    neutral.extend(neu)   
    pos,neg,neu = getNewsCard(competitor, days, newsCompetitor)
    positive.extend(pos)
    negative.extend(neg)
    neutral.extend(neu)
    pos,neg,neu = getNewsCard(hashtag, days, newsHashtag)
    positive.extend(pos)
    negative.extend(neg)
    neutral.extend(neu)
    pos,neg,neu = getNewsCard(brand, days, redditBrands)
    positive.extend(pos)
    negative.extend(neg)
    neutral.extend(neu)
    pos,neg,neu = getNewsCard(competitor, days, redditCompetitor)
    positive.extend(pos)
    negative.extend(neg)
    neutral.extend(neu)
    pos,neg,neu = getNewsCard(hashtag, days, redditHashtag)
    positive.extend(pos)
    negative.extend(neg)
    neutral.extend(neu)

    return positive,negative,neutral

    # tables = [newsBrands, newsCompetitor, newsHashtag, redditBrands, redditCompetitor, redditHashtag]
    # for table in tables:
    #     pos,neg,neu = getNewsCard(brand,table)
def getNewsCard(name: str, days : int, table: str):
    now = datetime.now()
    one_month_ago = now - timedelta(days=days)
    rows = session.query(table).filter(table.published_at >= one_month_ago, table.name == name).all()
    positive = []
    negative = []
    neutral = []

    for row in rows:
        result = sia.polarity_scores(row.content)
        # print(result)
        if result['compound'] >= 0.05 :
            positive.append(row)
                # content.append(positive)
        elif result['compound'] <= - 0.05 :
            negative.append(row)
            # content.append(negative)
        else :
            neutral.append(row)
    return positive,negative,neutral

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