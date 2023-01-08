# python -m uvicorn main:app --reload
import schema
from database import SessionLocal, engine, session
import model 
from model import projects, users, newsBrands, newsCompetitor, newsHashtag, redditBrands
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
from reddit import redditApi
import asyncio
from sentiment import getNews
from graphs import getNewsGraph, getGraphs
from cards import getCards
from newGraph import graph
origins = [
    
    "http://localhost:3000",
]
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model.Base.metadata.create_all(bind=engine)

def get_database_session():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
from fastapi import FastAPI, Request, Response, HTTPException
from pydantic import BaseModel



def add_project(string,):
    strSplit = string.split(',')
    keywords = strSplit
    project = projects(
    user_id=1,
    p_brand_name=keywords[0],
    p_competitor_name=keywords[1],
    p_hashtag=keywords[2],
    p_creation_at=datetime.utcnow(),
    p_update_at=datetime.utcnow()
    )

    # add_project( new_project)
    session.add(project)
    session.commit()
    session.refresh(project)
    return project

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

def apiCall(string):
    add_project(string)
    redditApi(string)
    return newsApi(string)  
class UserStringRequest(BaseModel):
    enterBrandCompetitorHashtag: str
    email : dict
@app.post("/createProject")
async def submit(request: Request, user_string_request: UserStringRequest):
    user_string = user_string_request.enterBrandCompetitorHashtag
    
    l1,l2,l3 = apiCall(user_string)
    userID = user_string_request.email['id']
    
    p_id = session.query(projects).filter(projects.user_id == userID).first()
    if p_id:
        project = session.query(projects).filter(projects.user_id == userID, projects.p_id == p_id.p_id).first()
        res = getNews(project.p_brand_name, project.p_competitor_name, project.p_hashtag) 
        await asyncio.sleep(1)
        return {"message" : "Success"}
    else:
        return {"message": "project not found"}
    

def add_user():
    user = users(
        u_name='shah',
        u_email='u_email@gmail.com',
        u_password='u_password',
        u_creation_at=datetime.utcnow()
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@app.get("/createUser")
def read_root(db: Session = Depends(get_database_session)):
    add_user()
   
    return {"message": 'user'} 
@app.get('/retrieved')
def get_news_brand_by_id():
    # Retrieve a single row from the newsBrands table with the specified id
    # news_brand = session.query(newsBrands).filter(newsBrands.id == 139).first()
    username = 'shah@gmail.com'
    password = 'Sasda@232gjh'
    user = session.query(users).filter(users.u_email == username, users.u_password == password).first()
    if user:
        return {"status": "success", "user_id": user.u_id}
    else:
        return {"status": "error", "message": "Invalid username or password"}
    return news_brand
@app.get('/insert')
def insertOne():
    session.bulk_insert_mappings(newsBrands, rows)
    session.commit()
    return {"inserted": 'success'}
@app.get('/newsBrand')    
def get_news_brands():
    # Retrieve all rows from the newsBrands table
    news_brands = session.query(newsBrands).all()
    return news_brands
class UserRequest(BaseModel):
    username: str
    password: str
    email: str

@app.post("/users/")
def create_user(request: Request, user_request: UserRequest):
    try:
        name = user_request.username
        password = user_request.password
        email = user_request.email

        user = users(
            u_name=name,
            u_password=password,
            u_email=email,
            u_creation_at=datetime.utcnow()
        )
            
    # Add the user to the database
        session.add(user)
        session.commit()
    except:
        session.rollback()
        # err =  HTTPException(status_code=500, detail="Failed to create user.")
        return {"message": 'Failed to create user'}
    # return {"name": name, "password": password}
    return {"message": "Successfully created user."}
class UserloginRequest(BaseModel):
    email: str
    password: str

@app.post("/login/")
def login(request: Request, user_request : UserloginRequest):
    try:
        email = user_request.email
        password = user_request.password
        user = session.query(users).filter(users.u_email == email, users.u_password == password).first()
        if user:
            return {"message": "Success", "user_id": user.u_id, "user_email": user.u_email, "username": user.u_name}
            # return {"message": "Success"}
        else:
            return {"status": "error", "message": "Invalid username or password"}
    except: 
        return {"message": 'Failed to create user'}

@app.get("/tables")
def list_tables(db: Session = Depends(get_database_session)):
    with engine.connect() as conn:
        result = conn.execute("SELECT table_name FROM INFORMATION_SCHEMA.TABLES WHERE table_schema='FIVER'")
        tables = [row[0] for row in result]
        return {"tables": tables}

@app.get('/sentiment')
def sent():
    try:
        user_id = 1
        p_id = 1
        project = session.query(projects).filter(projects.user_id == user_id, projects.p_id == p_id).first()
        res = getNews(project.p_brand_name, project.p_competitor_name, project.p_hashtag) 
        return res
    except:
        return {"message": "error"}
class sentimentGraphInput(BaseModel):
    u_id: int
    p_id: int
    days: int
@app.get('/sentimentGraph')
# def sentimentGraph(request : Request, user_request: sentimentGraphInput):
def sentimentGraph():
    # try:
    #     # your code here
    #     return {"message": "working"}
    # except:
    #     return {"message": "sentiment error"}
    try:
        user_id = 1
        p_id = 1
        days = 30
        project = session.query(projects).filter(projects.user_id == user_id, projects.p_id == p_id).first()
        res = getGraphs(project.p_brand_name, project.p_competitor_name, project.p_hashtag, days) 
        return res
    except:
        session.rollback()
        
        return {"message": "sentiment error"}

@app.get('/cards')
def card():
    try:
        user_id = 1
        p_id = 1
        days = 30
        project = session.query(projects).filter(projects.user_id == user_id, projects.p_id == p_id).first()
        res = getCards(project.p_brand_name, project.p_competitor_name, project.p_hashtag,days) 
        return res
    except:
        session.rollback()
        return {"message": "card error"}

@app.get('/graph')
def graphtest():
    # try:
        
        user_id = 1
        p_id = 1
        days = 30
        project = session.query(projects).filter(projects.user_id == user_id, projects.p_id == p_id).first()
        res = graph(project.p_brand_name, project.p_competitor_name, project.p_hashtag, days) 
        return {'message': res}
    # except:
        return {'err': 'some err occured'} 