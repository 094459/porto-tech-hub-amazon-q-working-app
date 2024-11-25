from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from .database import db

class Survey(db.Model):
    __tablename__ = 'surveys'

    survey_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="surveys")
    options = relationship("SurveyOption", back_populates="survey", cascade="all, delete-orphan")
    responses = relationship("SurveyResponse", back_populates="survey", cascade="all, delete-orphan")

class SurveyOption(db.Model):
    __tablename__ = 'survey_options'

    option_id = Column(Integer, primary_key=True, autoincrement=True)
    survey_id = Column(Integer, ForeignKey('surveys.survey_id', ondelete='CASCADE'), nullable=False)
    option_text = Column(String, nullable=False)
    option_order = Column(Integer, nullable=False)

    __table_args__ = (
        CheckConstraint('option_order BETWEEN 1 AND 5', name='check_option_order'),
    )

    survey = relationship("Survey", back_populates="options")
    responses = relationship("SurveyResponse", back_populates="option")

class SurveyResponse(db.Model):
    __tablename__ = 'survey_responses'

    response_id = Column(Integer, primary_key=True, autoincrement=True)
    survey_id = Column(Integer, ForeignKey('surveys.survey_id', ondelete='CASCADE'), nullable=False)
    option_id = Column(Integer, ForeignKey('survey_options.option_id', ondelete='CASCADE'), nullable=False)
    respondent_email = Column(String)
    response_date = Column(DateTime, default=datetime.utcnow)

    survey = relationship("Survey", back_populates="responses")
    option = relationship("SurveyOption", back_populates="responses")