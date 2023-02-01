import schema
from database import SessionLocal, engine, session, session1, session2, session3, session4, session5, session6
import model 
from model import projects, users, newsBrands, newsCompetitor, newsHashtag, redditBrands, projectSentiments, redditBrands, redditCompetitor, redditHashtag
from datetime import datetime
from fastapi import FastAPI
from fastapi import FastAPI, Depends, Request
from sqlalchemy.orm import Session
from sqlalchemy import exists
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import re
import requests
import json
import pandas as pd
from typing import List, Dict, Any
from datetime import datetime
import praw

def updateTables(keywords,date):
    try:
        newsApi(keywords,date)
        redditApi(keywords, date)
        return {"message": "successfully updated"}

    except:
        return {"Error": "Not Updated"}

def newsBrandInsert(db:session, rows: List[Dict[str, Any]]):
    db.bulk_insert_mappings(newsBrands, rows)
    db.commit()
def newsCompetitorInsert(db:session, rows: List[Dict[str, Any]]):
    db.bulk_insert_mappings(newsCompetitor, rows)
    db.commit()
def newsHashtagInsert(db:session, rows: List[Dict[str, Any]]):
    db.bulk_insert_mappings(newsHashtag, rows)
    db.commit()
def newsApi(keywords, last_date):
    # keywords = keywords.split(',')
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
    n_k1 = []
    n_k2 = []
    n_k3 = []
    for row in k1:
        if row['published_at'] > last_date:
            n_k1.append(row)
    for row in k2:
        if row['published_at'] > last_date:
            n_k2.append(row)
    for row in k3:
        if row['published_at'] > last_date:
            n_k3.append(row)  
    
    newsBrandInsert(session, n_k1)
    newsCompetitorInsert(session, n_k2)
    newsHashtagInsert(session, n_k3)
    session.close()
    return len(n_k1),len(n_k2),len(n_k3)



import threading

def redditBrandInsert(db:session1, rows: List[Dict[str, Any]]):
    db.bulk_insert_mappings(redditBrands, rows)
    db.commit()
def redditCompetitorInsert(db:session2, rows: List[Dict[str, Any]]):
    db.bulk_insert_mappings(redditCompetitor, rows)
    db.commit()
def redditHashtagInsert(db:session3, rows: List[Dict[str, Any]]):
    db.bulk_insert_mappings(redditHashtag, rows)
    db.commit()


def redditApi(keywords, last_date):
    # keywords = keywords.split(',')

    user_agent = "Ahmad 1.0 by /user/ahmad407"
    reddit = praw.Reddit(
        client_id = 'AzJE40YLWfAyY71kRGRSKA', 
        client_secret = 'g7BpsSTakcZvdRyhogi5S3PHA3ri8A', 
        user_agent = user_agent
    )
    limit = 2
    def api_call_1():
        session4 = SessionLocal()
        if not session4.query(exists().where(redditBrands.name == keywords[0])).scalar():
            subreddit = reddit.subreddit(keywords[0])
            k1 = []
            for submission in subreddit.hot(limit=limit):
                
                all_comments = submission.comments.list()
                
                for comment in all_comments:
                    if isinstance(comment, praw.models.reddit.comment.Comment):
                        data = {}
                        data['name'] = keywords[0]
                        data['description'] = subreddit.description
                        data['title'] = submission.title
                        data['source_name'] = submission.author
                        data['url'] = submission.url
                        data['author'] = comment.author
                        data['content'] = comment.body
                        date = str(datetime.fromtimestamp(comment.created_utc))
                        data['published_at'] = date
                        k1.append(data)
            n_k1 = []
            for row in k1:
                if row['published_at'] > last_date:
                    n_k1.append(row)
            session1 = SessionLocal()
            redditBrandInsert(session1, n_k1)

    def api_call_2():
        session5 = SessionLocal()
        if not session5.query(exists().where(redditCompetitor.name == keywords[1])).scalar():
            k2 = []
            subreddit = reddit.subreddit(keywords[1])
            for submission in subreddit.hot(limit=limit):
                
                all_comments = submission.comments.list()
                
                for comment in all_comments:
                    if isinstance(comment, praw.models.reddit.comment.Comment):
                        data = {}
                        data['name'] = keywords[1]
                        data['description'] = subreddit.description
                        data['title'] = submission.title
                        data['source_name'] = submission.author
                        data['url'] = submission.url
                        data['author'] = comment.author
                        data['content'] = comment.body
                        date = str(datetime.fromtimestamp(comment.created_utc))
                        
                        data['published_at'] = date
                        k2.append(data)
            n_k2 = []
            for row in k2:
                if row['published_at'] > last_date:
                    n_k2.append(row)
            session2 = SessionLocal()
            redditCompetitorInsert(session2, n_k2)

    def api_call_3():
        session6 = SessionLocal()
        if not session6.query(exists().where(redditHashtag.name == keywords[2])).scalar():
            k3 = []
            subreddit = reddit.subreddit(keywords[2])
            for submission in subreddit.hot(limit=limit):
                
                all_comments = submission.comments.list()
                
                for comment in all_comments:
                    if isinstance(comment, praw.models.reddit.comment.Comment):
                        data = {}
                        data['name'] = keywords[2]
                        data['description'] = subreddit.description
                        data['title'] = submission.title
                        data['source_name'] = submission.author
                        data['url'] = submission.url
                        data['author'] = comment.author
                        data['content'] = comment.body
                        date = str(datetime.fromtimestamp(comment.created_utc))
                        data['published_at'] = date
                        k3.append(data)
            n_k3 = []
            for row in k3:
                if row['published_at'] > last_date:
                    n_k3.append(row)
            session2 = SessionLocal()
            redditHashtagInsert(session2, n_k3)

    thread1 = threading.Thread(target=api_call_1)
    thread2 = threading.Thread(target=api_call_2)
    thread3 = threading.Thread(target=api_call_3)

    # start the threads
    thread1.start()
    thread2.start()
    thread3.start()

    # wait for the threads to finish
    thread1.join()
    thread2.join()
    thread3.join()