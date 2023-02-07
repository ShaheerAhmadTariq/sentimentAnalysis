# Sentiment Analysis 
# Description
In this project, you have created a full-stack web application that allows users to monitor brand mentions and analyze their sentiment across various news sources and social media platforms. The application consists of a ReactJS front-end and a FastAPI back-end, both connected to a MySQL database.

* Users can sign up and sign in to the application, and then enter keywords that represent the brands they want to monitor. The application uses the Reddit and NewsAPI to fetch data related to the entered keywords, which is then stored in the MySQL database.

* Once the data has been collected, the application performs sentiment analysis on the data using Vader, a popular library for sentiment analysis. The results of this analysis are then displayed as graphs on the frontend, which show the number of positive, negative, and neutral mentions of the brands over time.

* In addition, users can compare two projects to see how their brand mentions and sentiment have changed over time, and can also generate PDF reports of their projects for further analysis. The dashboard allows users to edit, delete, and update their projects, giving them full control over their data and insights.

# Technologies used:
## for frontend
        react js
## for backend
        fastapi
## for database
        mysql

# Setup 
## To run Frontend
    ### goto .\Sentiment\frontend
    $ yarn install --- this will install all required node modules
    $ npm start --- this will start the react app on localhost:3000
## To setup database
    create a new mysql database in mysql workbench by using following command
    $ CREATE DATABASE SENTIMENTS
    $ USE DATABASE SENTIMENTS
    Then goto .\Backend\Fastapi\database.py
    change line number 7 to 
    DATABASE_URL = "mysql+pymysql://"USERNAME":"PASSWORD"@localhost:3306/SENTIMENTS"
## To run Backend 
    ### goto .\Backend\Fastapi
    $ pip install -r requirements.txt --- this will install all required packages
    $ python -m uvicorn main:app --reload  --- this will start backend on port http://127.0.0.1:8000/


# API's used 
    Reddit (praw library)
    newsapi (https://newsapi.org/v2/everything)
