from sqlalchemy import create_engine, Enum
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from . import dataclasses
from jun_jobs_bot.settings import DB_CONNECT


engine = create_engine(DB_CONNECT)

session = sessionmaker(engine)

Base = declarative_base(engine)


class Language(Base):
    __tablename__ = 'Languages'

    id = Column(Integer, primary_key=True)
    language = Column(String(250), nullable=False)
    r = relationship('Statistics')


class Statistics(Base):
    __tablename__ = 'Statistics'

    id = Column(Integer, primary_key=True)
    language_id = Column(Integer, ForeignKey('Languages.id'))
    region_id = Column(Integer, ForeignKey('Regions.id'))
    site_id = Column(Integer, ForeignKey('Sites.id'), default=1)
    vacancies = Column(Integer)
    date = Column(Date)
    no_experience = Column(Integer, default=0)


class Regions(Base):
    __tablename__ = 'Regions'

    id = Column(Integer, primary_key=True)
    region = Column(String(255), nullable=False)
    r = relationship('Statistics')


class Sites(Base):
    __tablename__ = 'Sites'

    id = Column(Integer, primary_key=True)
    site = Column(String(255))
    r = relationship('Statistics')


class Users(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False, default='')
    experience = Column(Enum(dataclasses.ExperienceType))
    employed = Column(Enum(dataclasses.Employed))
    telegram_id = Column(Integer, nullable=False, unique=True)
    description = Column(String, default='', unique=False)
