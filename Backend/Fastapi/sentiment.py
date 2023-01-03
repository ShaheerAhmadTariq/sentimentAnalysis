from database import session
from model import newsBrands,newsCompetitor,newsHashtag,redditBrands,redditCompetitor,redditHashtag, projectSentiments
from typing import List, Dict, Any
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
from datetime import datetime
sia = SIA()
def getNews(brand: str, competitor: str, hashtag: str):
    brands = session.query(newsBrands).filter(newsBrands.name == brand).all()
    N_b_positive,N_b_negative,N_b_neutral = getSentiment(brands)
    competitors = session.query(newsCompetitor).filter(newsCompetitor.name == competitor).all()
    N_c_positive,N_c_negative,N_c_neutral = getSentiment(competitors)
    hashtags = session.query(newsHashtag).filter(newsHashtag.name == hashtag).all()
    N_h_positive,N_h_negative,N_h_neutral = getSentiment(hashtags)

    r_brands = session.query(redditBrands).filter(redditBrands.name == brand).all()
    R_b_positive,R_b_negative,R_b_neutral = getSentiment(r_brands)
    r_competitors = session.query(redditCompetitor).filter(redditCompetitor.name == competitor).all()
    R_c_positive,R_c_negative,R_c_neutral = getSentiment(r_competitors)
    r_hashtags = session.query(redditHashtag).filter(redditHashtag.name == hashtag).all()
    R_h_positive,R_h_negative,R_h_neutral = getSentiment(r_hashtags)

    p_Positve = N_b_positive + N_c_positive + N_h_positive + R_b_positive + R_c_positive + R_h_positive
    p_negative = N_b_negative + N_c_negative + N_h_negative + R_b_negative + R_c_negative + R_h_negative
    p_neutral = N_b_neutral + N_c_neutral + N_h_neutral + R_b_neutral + R_c_neutral + R_h_neutral

    n_p_brand_sentiments = {"positive":N_b_positive,"negative":N_b_negative, "neutral":N_b_neutral}
    n_p_competitor_sentiments = {"positive":N_c_positive,"negative":N_c_negative, "neutral":N_c_neutral}
    n_p_hashtag_sentiments = {"positive":N_h_positive,"negative":N_h_negative, "neutral":N_h_neutral}

    r_p_brand_sentiments = {"positive":R_b_positive,"negative":R_b_negative, "neutral":R_b_neutral}
    r_p_competitor_sentiments = {"positive":R_c_positive,"negative":R_c_negative, "neutral":R_c_neutral}
    r_p_hashtag_sentiments = {"positive":R_h_positive,"negative":R_h_negative, "neutral":R_h_neutral}

    n_p = N_b_positive + N_c_positive + N_h_positive
    n_n = N_b_negative + N_c_negative + N_h_negative
    n_neu = N_b_neutral + N_c_neutral + N_h_neutral

    r_p = R_b_positive + R_c_positive + R_h_positive
    r_n = R_b_negative + R_c_negative + R_h_negative
    r_neu = R_b_neutral + R_c_neutral + R_h_neutral

    n_p_sentiments = {"positive":n_p,"negative":n_n, "neutral":n_neu}
    r_p_sentiments = {"positive":r_p,"negative":r_n, "neutral":r_neu}

    p_sentiments = {"positive": p_Positve, "negative": p_negative, "neutral": p_neutral}
    sentiment = projectSentiments(
        project_id = 1,
        r_p_brand_sentiments = r_p_brand_sentiments,
        r_p_competitor_sentiments = r_p_competitor_sentiments,
        r_p_hashtag_sentiments = r_p_hashtag_sentiments,
        n_p_brand_sentiments = n_p_brand_sentiments,
        n_p_competitor_sentiments = n_p_competitor_sentiments,
        n_p_hashtag_sentiments = n_p_hashtag_sentiments,
        r_p_sentiments = r_p_sentiments,
        n_p_sentiments = n_p_sentiments,
        p_sentiments = p_sentiments
    )
    session.add(sentiment)
    session.commit()
    return {"message": "Success"}


def getSentiment(table: List[Dict[str, Any]]):
    content = []
    positive = 0
    negative = 0
    neutral = 0
    for data in table:
        # content.append(data['content'])
        
        # for comment in content:
        result = sia.polarity_scores(data.content)
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
