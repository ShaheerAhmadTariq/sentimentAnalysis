
import schema
from database import SessionLocal, engine, session, session1, session2, session6
import model
from model import projects, users, newsBrands, newsCompetitor, newsHashtag, redditBrands, projectSentiments
from datetime import datetime
from typing import List, Dict, Any
import re
import requests
import json
from sqlalchemy import exists, update

def newsBrandInsert(db:session, rows: List[Dict[str, Any]]):
    db.bulk_insert_mappings(newsBrands, rows)
    db.commit()
def newsCompetitorInsert(db:session, rows: List[Dict[str, Any]]):
    db.bulk_insert_mappings(newsCompetitor, rows)
    db.commit()
def newsHashtagInsert(db:session, rows: List[Dict[str, Any]]):
    db.bulk_insert_mappings(newsHashtag, rows)
    db.commit()
def newsApi(keywords):
    keywords = keywords.split(',')
    url = ('https://newsapi.org/v2/everything?q=' + ' OR '.join(keywords)) + '&language=en' + '&sortBy=relevancy' + '&apiKey=1a8e8d019bb0420e8aa011b382aa8f76' + '&pageSize=100'
    response = requests.get(url)
    data = json.loads(response.content)
    k1 = []
    k2 = []
    k3 = []

    for result in data['articles']:
        date = result["publishedAt"]
        date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ').date()
        article_data = {
                "source_id": 1,
                "source_name": result["source"]["name"],
                "author": result["author"],
                "title": result["title"],
                "description": result["description"],
                "url": result["url"],
                "url_to_image": result["urlToImage"],
                "published_at": date,
                "content": result["content"],
            }
        if re.search(keywords[0], result['content'], re.IGNORECASE):
            article_data['name'] = keywords[0]
            k1.append(article_data)
        elif re.search(keywords[1], result['content'], re.IGNORECASE):
            article_data['name'] = keywords[1]
            k2.append(article_data)
        elif re.search(keywords[2], result['content'], re.IGNORECASE):
            article_data['name'] = keywords[2]
            k3.append(article_data)

    if not session.query(exists().where(newsBrands.name == keywords[0])).scalar():
        newsBrandInsert(session, k1)
    if not session.query(exists().where(newsCompetitor.name == keywords[1])).scalar():
        newsCompetitorInsert(session, k2)
    if not session.query(exists().where(newsHashtag.name == keywords[2])).scalar():
        newsHashtagInsert(session, k3)


    session.close()
    return len(k1),len(k2),len(k3)