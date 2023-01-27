# python -m uvicorn main:app --reload
import schema
from database import SessionLocal, engine, session, session1, session2, session6
import model
from model import projects, users, newsBrands, newsCompetitor, newsHashtag, redditBrands, projectSentiments
from datetime import datetime
from fastapi import FastAPI
from fastapi import FastAPI, Depends, Request
from sqlalchemy.orm import Session
from sqlalchemy import exists, update
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
from graphs import getNewsGraph, getGraphs, getSingleLineChart
from cards import getCards
from newGraph import graph
from comparison import comparisonCountpie, comparisonLineChart
from update import updateTables
# from defalutCards import cardsDefault
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

@app.middleware("http")
async def db_session_middleware(request, call_next):
    response = None
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


def add_project(string,userID):
    strSplit = string.split(',')
    keywords = strSplit
    project = projects(
    user_id=userID,
    p_brand_name=keywords[0],
    p_competitor_name=keywords[1],
    p_hashtag=keywords[2],
    p_creation_at=datetime.utcnow(),
    p_update_at=datetime.utcnow()
    )

    # add_project( new_project)
    session1.add(project)
    session1.commit()
    session1.refresh(project)
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

def apiCall(string, userID):
    project = add_project(string, userID)
    redditApi(string)
    newsApi(string)
    return project.p_id


class UserStringRequest(BaseModel):
    enterBrandCompetitorHashtag: str
    email : dict
# Enter Keywords Page
# inputs are written in UserStringRequest
@app.post("/createProject")
# async def submit(request: Request, user_string_request: UserStringRequest):
async def submit(request: Request, user_string_request: UserStringRequest):
    user_string = user_string_request.enterBrandCompetitorHashtag
    userID = user_string_request.email['id']
    try:
        p_id = apiCall(user_string,userID)
        # p_id = session.query(projects).filter(projects.user_id == userID).first()
        # if p_id:
        project = session.query(projects).filter(projects.user_id == userID, projects.p_id == p_id).first()
        res = getNews(project.p_brand_name, project.p_competitor_name, project.p_hashtag,p_id)
        # await asyncio.sleep(1)
        return {"message" : "Success", "p_id": p_id}
    except:
        return {"message": "project not found"}

# def add_user():
#     user = users(
#         u_name='shah',
#         u_email='u_email@gmail.com',
#         u_password='u_password',
#         u_creation_at=datetime.utcnow()
#     )
#     session.add(user)
#     session.commit()
#     session.refresh(user)
#     return user

# @app.get("/createUser")
# def read_root(db: Session = Depends(get_database_session)):
#     user = add_user()
#     return {"message": 'user','u_id': user.u_id}
# @app.get('/retrieved')
# def get_news_brand_by_id():
#     # Retrieve a single row from the newsBrands table with the specified id
#     # news_brand = session.query(newsBrands).filter(newsBrands.id == 139).first()
#     username = 'shah@gmail.com'
#     password = 'Sasda@232gjh'
#     user = session.query(users).filter(users.u_email == username, users.u_password == password).first()
#     if user:
#         return {"status": "success", "user_id": user.u_id}
#     else:
#         return {"status": "error", "message": "Invalid username or password"}
#     return news_brand



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
    return {"message": "Successfully created user.", "user_id": user.u_id, "user_email": user.u_email, "username": user.u_name}
    # return {"message": "Successfully created user."}
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
@app.post('/sentimentGraph')
def sentimentGraph(request : Request, user_request: sentimentGraphInput):
# def sentimentGraph():

    try:
        user_id = user_request.u_id
        p_id = user_request.p_id
        days = user_request.days
        # user_id = 1
        # p_id = 1
        # days = 30
        project = session2.query(projects).filter(projects.user_id == user_id, projects.p_id == p_id).first()
        # print(project.p_brand_name)
        multiGraphs = getGraphs(project.p_brand_name, project.p_competitor_name, project.p_hashtag, days)
        singleGraph = getSingleLineChart(multiGraphs)
        return {'multiGraph':multiGraphs, "singleGraph":singleGraph}
    
    except:
        return {"multiGraph":{"positive":{"2023-01-14":8,"2023-01-12":16,"2023-01-19":48,"2023-01-05":32,"2023-01-11":48,"2023-01-18":96,"2023-01-25":108,"2023-01-17":112,"2023-01-13":0,"2022-12-29":32,"2023-01-03":32,"2023-01-04":80,"2023-01-08":32,"2022-12-30":32,"2023-01-02":18,"2023-01-09":0,"2023-01-15":32,"2023-01-23":100,"2023-01-07":32,"2023-01-16":16,"2023-01-24":180,"2023-01-21":32,"2023-01-20":16,"2023-01-01":0,"2023-01-26":54,"2023-01-27":68,"2023-01-06":0},"negative":{"2023-01-14":16,"2023-01-12":0,"2023-01-19":0,"2023-01-05":0,"2023-01-11":0,"2023-01-18":0,"2023-01-25":16,"2023-01-17":0,"2023-01-13":0,"2022-12-29":16,"2023-01-03":16,"2023-01-04":32,"2023-01-08":32,"2022-12-30":0,"2023-01-02":0,"2023-01-09":16,"2023-01-15":0,"2023-01-23":30,"2023-01-07":16,"2023-01-16":0,"2023-01-24":44,"2023-01-21":0,"2023-01-20":0,"2023-01-01":0,"2023-01-26":16,"2023-01-27":16,"2023-01-06":2},"neutral":{"2023-01-14":0,"2023-01-12":64,"2023-01-19":16,"2023-01-05":32,"2023-01-11":48,"2023-01-18":32,"2023-01-25":32,"2023-01-17":16,"2023-01-13":32,"2022-12-29":0,"2023-01-03":16,"2023-01-04":32,"2023-01-08":0,"2022-12-30":0,"2023-01-02":2,"2023-01-09":8,"2023-01-15":0,"2023-01-23":44,"2023-01-07":0,"2023-01-16":0,"2023-01-24":100,"2023-01-21":0,"2023-01-20":0,"2023-01-01":8,"2023-01-26":24,"2023-01-27":30,"2023-01-06":0}},"singleGraph":{"result":{"2023-01-14":24,"2023-01-12":80,"2023-01-19":64,"2023-01-05":64,"2023-01-11":96,"2023-01-18":128,"2023-01-25":156,"2023-01-17":128,"2023-01-13":32,"2022-12-29":48,"2023-01-03":64,"2023-01-04":144,"2023-01-08":64,"2022-12-30":32,"2023-01-02":20,"2023-01-09":24,"2023-01-15":32,"2023-01-23":174,"2023-01-07":48,"2023-01-16":16,"2023-01-24":324,"2023-01-21":32,"2023-01-20":16,"2023-01-01":8,"2023-01-26":94,"2023-01-27":114,"2023-01-06":2}}}
    
    # finally:
    #     session2.close()
        

class sentimentCardInput(BaseModel):
    u_id: int
    p_id: int
    days: int
@app.post('/cards')
# def card():
def card (request : Request, user_request: sentimentCardInput):
    try:
        user_id = user_request.u_id
        p_id = user_request.p_id
        days = user_request.days
        # user_id = 1
        # p_id = 1
        # days = 30
        project = session.query(projects).filter(projects.user_id == user_id, projects.p_id == p_id).first()
        res = getCards(project.p_brand_name, project.p_competitor_name, project.p_hashtag,days)
        return res
    except:
        # return cardsDefault
        return {"message": "card error"}

@app.get('/graph')
def graphtest():
    try:
        user_id = 1
        p_id = 1
        days = 30
        project = session.query(projects).filter(projects.user_id == user_id, projects.p_id == p_id).first()
        res = graph(project.p_brand_name, project.p_competitor_name, project.p_hashtag, days)
        session.close()
        session1.close()
        session2.close()
        return {'message': res}
    except:
        return {'err': 'some err occured while trying '}

class countComaparisonModel(BaseModel):
    u_id: int
    p_id1: int
    p_id2: int
    days: int
@app.post('/CountComparison/')
# def getCount():
def getCount (request : Request, user_request: countComaparisonModel):
    user_id = user_request.u_id
    p_id = user_request.p_id1
    days = user_request.days
    # user_id = 1
    # p_id = 1
    # days = 30

    try: 
        project = session.query(projects).filter(projects.user_id == user_id, projects.p_id == p_id).first()
        res = comparisonCountpie(project.p_brand_name, project.p_competitor_name, project.p_hashtag, days, p_id)
        p_id2 = user_request.p_id2
        
        # p_id2 = 3

        project = session1.query(projects).filter(projects.user_id == user_id, projects.p_id == p_id2).first()
        res2 = comparisonCountpie(project.p_brand_name, project.p_competitor_name, project.p_hashtag, days, p_id2)
        
        return {"project01": res, "project02": res2}
    except:
        return {"project01":{"name":"apple","Total":416,"Positive":243,"Negative":66,"NewsApi":70,"Reddit":346},"project02":{"name":"pepsi","Total":42,"Positive":22,"Negative":12,"NewsApi":37,"Reddit":5}}
        session1.rollback()
    finally:
        session.close()
class lineComaparisonModel(BaseModel):
    u_id: int
    p_id1: int
    p_id2: int
    days: int
@app.post('/comaprisonLineChart/')
# def getline():
def getline(request : Request, user_request: lineComaparisonModel):
    user_id = user_request.u_id
    p_id = user_request.p_id1
    days = user_request.days
    # user_id = 1
    # p_id = 1
    # days = 30
    try: 
        project = session.query(projects).filter(projects.user_id == user_id, projects.p_id == p_id).first()
        res = comparisonLineChart(project.p_brand_name, project.p_competitor_name, project.p_hashtag, days)
        p_id = user_request.p_id2
        
        # p_id = 3
        project = session.query(projects).filter(projects.user_id == user_id, projects.p_id == p_id).first()
        res2 = comparisonLineChart(project.p_brand_name, project.p_competitor_name, project.p_hashtag, days)
        
        result =  {"project01": res, "project02": res2}
        result["project01"] = sorted(result["project01"], key=lambda x: datetime.strptime(next(iter(x)), "%Y-%m-%d"))
        result["project02"] = sorted(result["project01"], key=lambda x: datetime.strptime(next(iter(x)), "%Y-%m-%d"))
        return result
    except:
        return {"project01":[{"2022-12-29":30},{"2022-12-30":6},{"2023-01-02":6},{"2023-01-03":12},{"2023-01-04":24},{"2023-01-05":24},{"2023-01-06":6},{"2023-01-08":12},{"2023-01-09":6},{"2023-01-10":6},{"2023-01-11":48},{"2023-01-12":48},{"2023-01-13":18},{"2023-01-14":12},{"2023-01-15":12},{"2023-01-17":30},{"2023-01-18":30},{"2023-01-19":18},{"2023-01-20":6},{"2023-01-21":12},{"2023-01-23":18},{"2023-01-24":6},{"2023-01-25":6}],"project02":[{"2022-12-29":30},{"2022-12-30":6},{"2023-01-02":6},{"2023-01-03":12},{"2023-01-04":24},{"2023-01-05":24},{"2023-01-06":6},{"2023-01-08":12},{"2023-01-09":6},{"2023-01-10":6},{"2023-01-11":48},{"2023-01-12":48},{"2023-01-13":18},{"2023-01-14":12},{"2023-01-15":12},{"2023-01-17":30},{"2023-01-18":30},{"2023-01-19":18},{"2023-01-20":6},{"2023-01-21":12},{"2023-01-23":18},{"2023-01-24":6},{"2023-01-25":6}]}

class getProjectsModel(BaseModel):
    u_id: int
@app.post('/getProjects')
def getProjects(request : Request, user_request: getProjectsModel):
    try :
        user_id = user_request.u_id
        project = session.query(projects).filter(projects.user_id == user_id).all()
        return project
    except:
        return {"error while fetching projects"}

class deleteProjectModel(BaseModel):
    u_id: int
    p_id: int
@app.post('/deleteProject')
def deleteProjectfunction(request : Request, user_request: deleteProjectModel):
# def deleteProjectfunction():
    # Delete a specific project and its associated projectSentiments by its id
    # project_id = 39
    user_id = user_request.u_id
    project_id = user_request.p_id
    project = session.query(projects).filter(projects.user_id == user_id).all()
    for p in project:
        if p.p_id == project_id:
            session.query(projectSentiments).filter(projectSentiments.project_id.in_(session.query(projects.p_id).filter(projects.p_id == project_id))).delete(synchronize_session='fetch')
            session.query(projects).filter(projects.p_id == project_id).delete()
            session.commit()
            return {'message': 'successfully deleted'}
    return {'message': 'Project not found'}

class updateProjectModel(BaseModel):
    u_id: int
    p_id: int
@app.post('/updateProject')
# def projectupdatefunction():
def projectupdatefunction(request : Request, user_request: updateProjectModel):
    # p_id =  28
    # user_id = 1
    try:
        user_id = user_request.u_id
        p_id = user_request.p_id
        project = session.query(projects).filter(projects.user_id == user_id, projects.p_id == p_id).first()
        creationDate = project.p_creation_at
        current_date = datetime.now().date()
        time = current_date - creationDate
        if time.days > 1:
            res = updateTables([project.p_brand_name, project.p_competitor_name, project.p_hashtag], creationDate)
        # return {"time": time.days, "res": res}
        return {'message': "Successfully updated"}
    except:
        return {'message': "Project Not Found"}

class sentimentGraphSingleInput(BaseModel):
    u_id: int
    p_id: int
    days: int

@app.post('/mentionsSingleLineChart')
def getline(request : Request, user_request: sentimentGraphSingleInput):
# def getline():

    # user_id = 1
    # p_id = 1
    # days = 30
    user_id = user_request.u_id
    p_id = user_request.p_id
    days = user_request.days
    project = session.query(projects).filter(projects.user_id == user_id, projects.p_id == p_id).first()
    res = comparisonLineChart(project.p_brand_name, project.p_competitor_name, project.p_hashtag, days)
    return res

class forgetPasswordModel(BaseModel):
    u_email: str
    p_id: int
@app.post('/forgetPassword')
def getPassword(request : Request, user_request: forgetPasswordModel):
# def updatePassword():
    # user_id = user_request.u_id
    p_id = user_request.p_id
    user_email = user_request.u_email
    try:
        # user_id = 1
        # user_email = 'shah@gmail.com'
        # p_id = 'Qwerty12@34'
        session.query(users).filter(users.u_email == user_email).update({users.u_password: p_id})
        session.commit()
        return {"message":"password updated"}
    except:
        return {"message":"User not found"}


# Report page
class reportPieModel(BaseModel):
    u_id: int
    p_id1: int
@app.post('/reportPieChart/')
def reportPie(request : Request, user_request: reportPieModel):
    user_id = user_request.u_id
    p_id = user_request.p_id1
    days = 30
    project = session.query(projects).filter(projects.user_id == user_id, projects.p_id == p_id).first()
    res = comparisonCountpie(project.p_brand_name, project.p_competitor_name, project.p_hashtag, days, p_id)
    return {"project01": res}
