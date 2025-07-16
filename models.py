from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class Session(Base):
    __tablename__ = 'sessions'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    arrows_per_set = Column(Integer)
    sets = relationship("ArrowSet", back_populates="session", cascade="all, delete-orphan")

class ArrowSet(Base):
    __tablename__ = 'arrow_sets'
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey('sessions.id'))
    session = relationship("Session", back_populates="sets")
    arrows = relationship("Arrow", back_populates="arrow_set", cascade="all, delete-orphan")

class Arrow(Base):
    __tablename__ = 'arrows'
    id = Column(Integer, primary_key=True)
    set_id = Column(Integer, ForeignKey('arrow_sets.id'))
    x = Column(Float)
    y = Column(Float)
    score = Column(Integer)
    arrow_set = relationship("ArrowSet", back_populates="arrows")
