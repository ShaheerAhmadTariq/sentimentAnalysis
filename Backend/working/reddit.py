from model import redditBrands, redditCompetitor, redditHashtag
import praw
from datetime import datetime
from database import session
from typing import List, Dict, Any
from sqlalchemy import exists
import threading

def redditBrandInsert(db:session, rows: List[Dict[str, Any]]):
    db.bulk_insert_mappings(redditBrands, rows)
    db.commit()
def redditCompetitorInsert(db:session, rows: List[Dict[str, Any]]):
    db.bulk_insert_mappings(redditCompetitor, rows)
    db.commit()
def redditHashtagInsert(db:session, rows: List[Dict[str, Any]]):
    db.bulk_insert_mappings(redditHashtag, rows)
    db.commit()


def redditApi(keywords):
    keywords = keywords.split(',')

    user_agent = "Ahmad 1.0 by /user/ahmad407"
    reddit = praw.Reddit(
        client_id = 'AzJE40YLWfAyY71kRGRSKA', 
        client_secret = 'g7BpsSTakcZvdRyhogi5S3PHA3ri8A', 
        user_agent = user_agent
    )
    limit = 10
    def api_call_1():
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
        if not session.query(exists().where(redditBrands.name == keywords[0])).scalar():
            redditBrandInsert(session, k1)

    def api_call_2():
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
        if not session.query(exists().where(redditCompetitor.name == keywords[1])).scalar():
            redditCompetitorInsert(session, k2)

    def api_call_3():
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
        if not session.query(exists().where(redditHashtag.name == keywords[2])).scalar():
            redditHashtagInsert(session, k3)

    # create three threads, one for each API call
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



# def redditApi(keywords):
#     keywords = keywords.split(',')
    
#     user_agent = "Ahmad 1.0 by /user/ahmad407"
#     reddit = praw.Reddit(
#         client_id = 'AzJE40YLWfAyY71kRGRSKA', 
#         client_secret = 'g7BpsSTakcZvdRyhogi5S3PHA3ri8A', 
#         user_agent = user_agent
#     )
#     limit = 10
#     # keywords = ["apple", "alienware", "lenovo"]
#     subreddit = reddit.subreddit(keywords[0])
#     k1 = []
#     for submission in subreddit.hot(limit=limit):
        
#         all_comments = submission.comments.list()
        
#         for comment in all_comments:
#             if isinstance(comment, praw.models.reddit.comment.Comment):
#                 data = {}
#                 data['name'] = keywords[0]
#                 data['description'] = subreddit.description
#                 data['title'] = submission.title
#                 data['source_name'] = submission.author
#                 data['url'] = submission.url
#                 data['author'] = comment.author
#                 data['content'] = comment.body
#                 date = str(datetime.fromtimestamp(comment.created_utc))
#                 data['published_at'] = date
#                 k1.append(data)
        

#     k2 = []
#     subreddit = reddit.subreddit(keywords[1])
#     for submission in subreddit.hot(limit=limit):
        
#         all_comments = submission.comments.list()
        
#         for comment in all_comments:
#             if isinstance(comment, praw.models.reddit.comment.Comment):
#                 data = {}
#                 data['name'] = keywords[1]
#                 data['description'] = subreddit.description
#                 data['title'] = submission.title
#                 data['source_name'] = submission.author
#                 data['url'] = submission.url
#                 data['author'] = comment.author
#                 data['content'] = comment.body
#                 date = str(datetime.fromtimestamp(comment.created_utc))
                
#                 data['published_at'] = date
#                 k2.append(data)
#     k3 = []
#     subreddit = reddit.subreddit(keywords[2])
#     for submission in subreddit.hot(limit=limit):
        
#         all_comments = submission.comments.list()
        
#         for comment in all_comments:
#             if isinstance(comment, praw.models.reddit.comment.Comment):
#                 data = {}
#                 data['name'] = keywords[2]
#                 data['description'] = subreddit.description
#                 data['title'] = submission.title
#                 data['source_name'] = submission.author
#                 data['url'] = submission.url
#                 data['author'] = comment.author
#                 data['content'] = comment.body
#                 date = str(datetime.fromtimestamp(comment.created_utc))
#                 data['published_at'] = date
#                 k3.append(data)

#     if not session.query(exists().where(redditBrands.name == keywords[0])).scalar():
#         redditBrandInsert(session, k1)
#     if not session.query(exists().where(redditCompetitor.name == keywords[1])).scalar():
#         redditCompetitorInsert(session, k2)
#     if not session.query(exists().where(redditHashtag.name == keywords[2])).scalar():
#         redditHashtagInsert(session, k3)
