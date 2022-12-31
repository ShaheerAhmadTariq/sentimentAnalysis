from sqlalchemy.schema import Column, ForeignKey
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.types import String, Integer, Text
from sqlalchemy.orm import relationship
from database import Base


class users(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}

    u_id = Column(Integer, primary_key=True)
    u_name = Column(String(100))
    u_email = Column(String(50), unique=True)
    u_password = Column(String(200))
    u_creation_at = Column(DateTime, default=datetime.utcnow)


class projects(Base):
    __tablename__ = "projects"
    __table_args__ = {'extend_existing': True}

    p_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(users.u_id, ondelete="CASCADE"), nullable=False)
    user_project = relationship(users)
    p_brand_name = Column(String(100), unique=False, nullable=True)
    p_competitor_name = Column(String(100), unique=False, nullable=True)
    p_hashtag = Column(String(100), unique=False, nullable=True)
    p_creation_at = Column(DateTime, default=datetime.utcnow)
    p_update_at = Column(DateTime, default=datetime.utcnow)
    
class redditBrands(Base):
    __tablename__ = "redditBrands"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    
    source_name = Column(String(255))
    author = Column(String(255))
    title = Column(Text)
    description = Column(Text)
    url = Column(String(255))
    
    published_at = Column(DateTime)
    content = Column(Text)
    name = Column(String(255))

class redditCompetitor(Base):
    __tablename__ = "redditCompetitor"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    
    source_name = Column(String(255))
    author = Column(String(255))
    title = Column(Text)
    description = Column(Text)
    url = Column(String(255))
    
    published_at = Column(DateTime)
    content = Column(Text)
    name = Column(String(255))

class redditHashtag(Base):
    __tablename__ = "redditHashtag"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    
    source_name = Column(String(255))
    author = Column(String(255))
    title = Column(Text)
    description = Column(Text)
    url = Column(String(255))
    
    published_at = Column(DateTime)
    content = Column(Text)
    name = Column(String(255))

class newsBrands(Base):
    __tablename__ = "newsBrands"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    source_id = Column(Integer)
    source_name = Column(String(255))
    author = Column(String(255))
    title = Column(String(255))
    description = Column(Text)
    url = Column(String(255))
    url_to_image = Column(String(255))
    published_at = Column(DateTime)
    content = Column(Text)
    name = Column(String(255))

class newsCompetitor(Base):
    __tablename__ = "newsCompetitor"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    source_id = Column(Integer)
    source_name = Column(String(255))
    author = Column(String(255))
    title = Column(String(255))
    description = Column(Text)
    url = Column(String(255))
    url_to_image = Column(String(255))
    published_at = Column(DateTime)
    content = Column(Text)
    name = Column(String(255))

class newsHashtag(Base):
    __tablename__ = "newsHashtag"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    source_id = Column(Integer)
    source_name = Column(String(255))
    author = Column(String(255))
    title = Column(String(255))
    description = Column(Text)
    url = Column(String(255))
    url_to_image = Column(String(255))
    published_at = Column(DateTime)
    content = Column(Text)
    name = Column(String(255))
    
class projectSentiments(Base):
    __tablename__ = "projectSentiments"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey(projects.p_id, ondelete="CASCADE"), nullable=False)
    project_sentiments = relationship(projects)
    
    r_p_brand_sentiments = Column(JSON)
    r_p_competitor_sentiments = Column(JSON)
    r_p_hashtag_sentiments = Column(JSON)
    
    n_p_brand_sentiments = Column(JSON)
    n_p_competitor_sentiments = Column(JSON)
    n_p_hashtag_sentiments = Column(JSON)
    
    r_p_sentiments = Column(JSON)
    n_p_sentiments = Column(JSON)
    p_sentiments = Column(JSON)