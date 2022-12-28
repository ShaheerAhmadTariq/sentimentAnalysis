from db_config import Base
from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from _datetime import datetime
from sqlalchemy.orm import relationship


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
    p_brand_name = Column(String(100), unique=True, nullable=True)
    p_competitor_name = Column(String(100), unique=True, nullable=True)
    p_hashtag = Column(String(100), unique=True, nullable=True)
    p_creation_at = Column(DateTime, default=datetime.utcnow)
    p_update_at = Column(DateTime, default=datetime.utcnow)


class redditMentions(Base):
    __tablename__ = "redditMentions"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey(projects.p_id, ondelete="CASCADE"), nullable=False)
    reddit_mentions = relationship(projects)
    r_p_brand_mentions = Column(JSON)
    r_p_competitor_mentions = Column(JSON)
    r_p_hashtag_mentions = Column(JSON)


class newsMentions(Base):
    __tablename__ = "newsMentions"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey(projects.p_id, ondelete="CASCADE"), nullable=False)
    news_mentions = relationship(projects)
    n_p_brand_mentions = Column(JSON)
    n_p_competitor_mentions = Column(JSON)
    n_p_hashtag_mentions = Column(JSON)


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

