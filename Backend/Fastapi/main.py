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
from newsApi import newsApi
from sentiment import getNews, handleExceptionProjectSentiment
from graphs import getNewsGraph, getGraphs, getSingleLineChart, handleExceptionSentimentGraph
from cards import getCards
from newGraph import graph
from comparison import comparisonCountpie, comparisonLineChart, handleExceptiongetCount, handleExceptionLineChart, handleExceptionPieChart
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

def apiCall(string, userID):
    project = add_project(string, userID)
    redditApi(string)
    newsApi(string)
    return project.p_id


class UserStringRequest(BaseModel):
    enterBrandCompetitorHashtag: str
    email : dict

@app.post("/createProject")
# async def submit(request: Request, user_string_request: UserStringRequest):
def submit(request: Request, user_string_request: UserStringRequest):
    user_string = user_string_request.enterBrandCompetitorHashtag
    userID = user_string_request.email['id']
    
    try:
        # p_id = 1
        p_id = apiCall(user_string,userID)
        project = session6.query(projects).filter(projects.user_id == userID, projects.p_id == p_id).first()
        res = getNews(project.p_brand_name, project.p_competitor_name, project.p_hashtag,p_id)
       
        return {"message" : "Success", "p_id": p_id}
    except:
        # project = session.query(projects).filter(projects.user_id == userID, projects.p_id == p_id).first()
        # handleExceptionProjectSentiment(project.p_brand_name, project.p_competitor_name, project.p_hashtag,p_id)
        # return {"message" : "Success", "p_id": p_id}
        return {"message": "project not found"}



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
        return handleExceptionSentimentGraph()


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
        return handleExceptiongetCount()
    
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
        p_id2 = user_request.p_id2

        # p_id2 = 3
        project2 = session1.query(projects).filter(projects.user_id == user_id, projects.p_id == p_id2).first()
        res2 = comparisonLineChart(project2.p_brand_name, project2.p_competitor_name, project2.p_hashtag, days)

        result =  {"project01": res, "project02": res2}
        result["project01"] = sorted(result["project01"], key=lambda x: datetime.strptime(next(iter(x)), "%Y-%m-%d"))
        result["project02"] = sorted(result["project02"], key=lambda x: datetime.strptime(next(iter(x)), "%Y-%m-%d"))
        return result
    except:
        return handleExceptionLineChart()
        
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
    p_id: str
@app.post('/forgetPassword')
def getPassword(request : Request, user_request: forgetPasswordModel):
# def updatePassword():
    # user_id = user_request.u_id
    p_id = user_request.p_id
    user_email = user_request.u_email
    print("user email: ",user_email,p_id)
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
# def reportPie():
    user_id = user_request.u_id
    p_id = user_request.p_id1
    # user_id = 1
    # p_id = 1
    days = 30
    try: 
        project = session6.query(projects).filter(projects.user_id == user_id, projects.p_id == p_id).first()
        res = comparisonCountpie(project.p_brand_name, project.p_competitor_name, project.p_hashtag, days, p_id)
        return {"project01": res}
    except:
        return handleExceptionPieChart()
