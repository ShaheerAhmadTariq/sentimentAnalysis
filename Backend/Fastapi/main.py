# python -m uvicorn main:app --reload
import schema
from database import SessionLocal, engine, session
import model 
from model import projects, users, newsBrands, newsCompetitor, newsHashtag, namesNews
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
def brand_exists(session, brand_name):
    return session.query(exists().where(namesNews.brand_name == brand_name)).scalar()
def competitor_exists(session, brand_name):
    return session.query(exists().where(namesNews.competitor_name == brand_name)).scalar()
def hashtag_exists(session, brand_name):
    return session.query(exists().where(namesNews.hashtag_name == brand_name)).scalar()
def namesNamesInsert(db: Session, brand_name: str, competitor_name: str, hashtag_name: str):
    name = namesNews(brand_name=brand_name, competitor_name=competitor_name, hashtag_name=hashtag_name)
    db.add(name)
    db.commit()

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

        if re.search(keywords[0], result['content'], re.IGNORECASE):
            # print("Match found!",result)
            k1.append({'n_p_brand_mentions':result})
        elif re.search(keywords[1], result['content'], re.IGNORECASE):
            k2.append({'n_p_competitor_mentions':result})
        elif re.search(keywords[2], result['content'], re.IGNORECASE):
            k3.append({'n_p_hashtag_mentions':result})
    # exists = record_exists(session, 'Lenovo')
    if not brand_exists(session, keywords[0]):
        newsBrandInsert(session, k1)
    if not competitor_exists(session, keywords[1]):
        newsCompetitorInsert(session, k2)
    if not hashtag_exists(session, keywords[2]):
        newsHashtagInsert(session, k3)
    namesNamesInsert(session, keywords[0], keywords[1], keywords[2])
    
    session.close()
    return len(k1),len(k2),len(k3)

def apiCall(string):
    add_project(string)
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
@app.post("/string")
def submit(request: Request, user_string_request: UserStringRequest):
    user_string = user_string_request.user_string
    # apiCall(user_string)
    l1,l2,l3 = apiCall(user_string)
    
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


    # Insert multiple rows into the newsBrands table
#     rows = [
#         {'n_p_brand': 'brand1', 'n_p_brand_mentions': {'mention1': 'mention2'}},
#         {'n_p_brand': 'brand2', 'n_p_brand_mentions': {'mention3': 'mention4'}},
#         {'n_p_brand': 'brand3', 'n_p_brand_mentions': {'mention5': 'mention6'}},
#         {'n_p_brand': 'razer',
#  'n_p_brand_mentions': {'source': {'id': None, 'name': 'Windows Central'},
#   'author': 'jd.levite@futurenet.com (John Levite)',
#   'title': 'Cyber Monday is your one chance to save on a Razer Blade 15 with RTX 3080 Ti graphics',
#   'description': "Razer laptops are expensive for reason: they're awesome. Save now in one of the only deals you'll ever see for this laptop.",
#   'url': 'https://www.windowscentral.com/hardware/laptops/cyber-monday-is-your-one-chance-to-save-on-a-razer-blade-15-with-rtx-3080-ti-graphics',
#   'urlToImage': 'https://cdn.mos.cms.futurecdn.net/Mb8ZMEBz7qTGjj4ugJKu9Z-1200-80.jpg',
#   'publishedAt': '2022-11-28T15:40:59Z',
#   'content': "If you want a gaming laptop that doesn't pull any punches, Razer is usually where you want to go. Of course, they don't pull any punches on price either except for Cyber Monday where you can actually… [+1544 chars]"}},
#   {'n_p_brand': 'razer',
#  'n_p_brand_mentions': {'source': {'id': None, 'name': 'Digital Trends'},
#   'author': 'Jacob Roach',
#   'title': 'The ROG Zephyrus G14 infuriates me, but its still my favorite gaming laptop of 2022',
#   'description': 'Even after repairs, multiple bugs, and borked software updates, the Asus ROG Zephyrus G14 is my favorite gaming laptop of 2022.',
#   'url': 'https://www.digitaltrends.com/computing/asus-rog-zephyrus-g14-favorite-gaming-laptop-2022/',
#   'urlToImage': 'https://www.digitaltrends.com/wp-content/uploads/2022/12/zephyrus-g14-favorite-tech-2022-06.jpg?resize=1200%2C630&p=1',
#   'publishedAt': '2022-12-21T16:00:00Z',
#   'content': 'Gaming laptops are antithetical to how I play games, and despite my best efforts, ve never had great luck with them. Thats why I sold my 2019 Razer Blade 15 to buy a Steam Deck early in the year.\r… [+7519 chars]'}}
#     ]

    rows = [
        {'n_p_brand_mentions': {'source': {'id': None, 'name': 'Windows Central'},
  'author': 'jd.levite@futurenet.com (John Levite)',
  'title': 'Cyber Monday is your one chance to save on a Razer Blade 15 with RTX 3080 Ti graphics',
  'description': "Razer laptops are expensive for reason: they're awesome. Save now in one of the only deals you'll ever see for this laptop.",
  'url': 'https://www.windowscentral.com/hardware/laptops/cyber-monday-is-your-one-chance-to-save-on-a-razer-blade-15-with-rtx-3080-ti-graphics',
  'urlToImage': 'https://cdn.mos.cms.futurecdn.net/Mb8ZMEBz7qTGjj4ugJKu9Z-1200-80.jpg',
  'publishedAt': '2022-11-28T15:40:59Z',
  'content': "If you want a gaming laptop that doesn't pull any punches, Razer is usually where you want to go. Of course, they don't pull any punches on price either except for Cyber Monday where you can actually… [+1544 chars]"}},
  {'n_p_brand_mentions': {'source': {'id': None, 'name': 'Windows Central'},
  'author': 'sendicott47@outlook.com (Sean Endicott)',
  'title': 'This Razer Raptor 27 Cyber Monday monitor deal is so good we thought it was a mistake',
  'description': 'The Razer Raptor 27 with a 165Hz refresh rate is on sale for Cyber Monday. The newer model is even cheaper than its predecessor that has a lower refresh rate.',
  'url': 'https://www.windowscentral.com/gaming/this-razer-raptor-27-cyber-monday-monitor-deal-is-so-good-we-thought-it-was-a-mistake',
  'urlToImage': 'https://cdn.mos.cms.futurecdn.net/XUQLLgZbcyWjrd45RpJuFG-1200-80.png',
  'publishedAt': '2022-11-28T15:42:29Z',
  'content': "The Razer Raptor 27 goes toe-to-toe with the best gaming monitors on the market. Right now, it's also one of the best Cyber Monday deals.\xa0\r\nUsually, the latest and greatest version of an item costs m… [+1565 chars]"}}
    ]
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



@app.get("/tables")
def list_tables(db: Session = Depends(get_database_session)):
    with engine.connect() as conn:
        result = conn.execute("SELECT table_name FROM INFORMATION_SCHEMA.TABLES WHERE table_schema='FIVER'")
        tables = [row[0] for row in result]
        return {"tables": tables}