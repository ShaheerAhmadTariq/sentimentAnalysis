# Sentiment Analysis 
# Description
    I have created a web application that allows users to sign up and sign in, after which they can enter keywords related to brand names. 
    The application uses Reddit and NewsAPI to fetch data related to the brand names and stores the results in the database. 
    Sentiment analysis is performed on the fetched data using the Vader library, 
    and the results are displayed in the form of a graph showing the positive, negative, and neutral sentiments, along with the number of mentions.
    The user can compare two projects and also generate a PDF report of their projects. 
    A dashboard is provided for the user to edit, delete, and update their projects.

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
