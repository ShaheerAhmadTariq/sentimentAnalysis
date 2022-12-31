# python -m uvicorn main:app --reload
import schema
from database import SessionLocal, engine, session
import model 
from model import projects, users, newsBrands, newsCompetitor, newsHashtag
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
class UserStringRequest(BaseModel):
    user_string: str


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
# def brand_exists(session, brand_name):
#     return session.query(exists().where(namesNews.brand_name == brand_name)).scalar()
# def competitor_exists(session, brand_name):
#     return session.query(exists().where(namesNews.competitor_name == brand_name)).scalar()
# def hashtag_exists(session, brand_name):
#     return session.query(exists().where(namesNews.hashtag_name == brand_name)).scalar()
# def namesNamesInsert(db: Session, brand_name: str, competitor_name: str, hashtag_name: str):
#     name = namesNews(brand_name=brand_name, competitor_name=competitor_name, hashtag_name=hashtag_name)
#     db.add(name)
#     db.commit()

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
    # url = ('https://newsapi.org/v2/everything?q=' + ' OR '.join(keywords)) + '&language=en' + '&sortBy=relevancy' + '&apiKey=1a8e8d019bb0420e8aa011b382aa8f76' + '&pageSize=100'

    # response = requests.get(url)

    # data = json.loads(response.content)
    # if len(strSplit) == 3:
    #     k1 = []
    #     k2 = []
    #     k3 = []
    #     for key,_ in data.items():
    #         totalResults = []
    #         for result in data['articles']:
    #             # print(result)
    #             if re.search(keywords[0], result['content'], re.IGNORECASE):
    #                 # print("Match found!",result)
    #                 k1.append(result)
    #             elif re.search(keywords[1], result['content'], re.IGNORECASE):
    #                 k2.append(result)
    #             elif re.search(keywords[2], result['content'], re.IGNORECASE):
    #                 k3.append(result)
@app.post("/createProject")
async def submit(request: Request, user_string_request: UserStringRequest):
    user_string = user_string_request.user_string
    # apiCall(user_string)
    l1,l2,l3 = apiCall(user_string)
    await asyncio.sleep(1)
    # if not user_string:
    #     raise HTTPException(status_code=422, detail="User string is required")
    # Do something with the user string here, such as storing it in a database or sending it to another API
    return {"l1": l1, "l2": l2, 'l3': l3}
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
    # newMovie = Movie(name='Alice', desc="thisafa", type= 'fkajf', url='kjksvksv', rating=7)
    # db.add(newMovie)
    # db.commit()
    # Movie.insert().values(name='Alice', desc="thisafa", type= 'fkajf', url='kjksvksv', rating=7)
    
    # users = db.query(Movie).all()
    # for user in users:
    #     print(f'Name: {user.name}')
    #     return {"message": user.name}
    #     break
    return {"message": 'user'} 
@app.get('/retrieved')
def get_news_brand_by_id():
    # Retrieve a single row from the newsBrands table with the specified id
    news_brand = session.query(newsBrands).filter(newsBrands.id == 139).first()
    return news_brand

@app.get('/insert')
def insertOne():
    # newsApi('lenovo,reno,iphone')

    
    # df = pd.DataFrame.from_dict(rows)
    # rows = df.to_dict(orient='records')
    session.bulk_insert_mappings(newsBrands, rows)
    session.commit()


    
    # new_brand = {"n_p_brand": 'brand',
    # "n_p_brand_mentions": {"key1": "value1", "key2": "value2"}}
    # new_brand = newsBrands(**new_brand)
    # session.add(new_brand)
    # session.commit()
    # session.refresh(new_brand)
    return {"inserted": 'success'}
@app.get('/newsBrand')    
def get_news_brands():
    # Retrieve all rows from the newsBrands table
    news_brands = session.query(newsBrands).all()
    return news_brands

@app.post("/users/")
def create_user(request: Request):
    # Get the name and password from the request
    name = request.form["name"]
    password = request.form["password"]
    email = request.form["email"]

    # Create a new user object
    user = users(
        u_name=name,
        u_password=password,
        u_email=email,
        u_creation_at=datetime.utcnow()
    )
    try:
    # Add the user to the database
        session.add(user)
        session.commit()
    except:
        session.rollback()
        # err =  HTTPException(status_code=500, detail="Failed to create user.")
        return {"message": 'Failed to create user'}
    # return {"name": name, "password": password}
    return {"message": "Successfully created user."}

@app.post("/login/")
def login(request: Request):
    username = request.form["name"]
    password = request.form["password"]
    user = session.query(users).filter(users.u_name == username, users.u_password == password).first()
    if user:
        return {"status": "success", "user_id": user.u_id}
    else:
        return {"status": "error", "message": "Invalid username or password"}

@app.get("/tables")
def list_tables(db: Session = Depends(get_database_session)):
    with engine.connect() as conn:
        result = conn.execute("SELECT table_name FROM INFORMATION_SCHEMA.TABLES WHERE table_schema='FIVER'")
        tables = [row[0] for row in result]
        return {"tables": tables}