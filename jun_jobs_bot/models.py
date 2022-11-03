from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from jun_jobs_bot.settings import DB_USERNAME, DB_PASSWORD, \
    HOST, PORT, DATABASE

engine = create_engine('postgresql+psycopg2://zrccggtqrkphaw:02a4d05dff7828f2c829633feeab670259f29a8b23022c73e7ab3f7e78fb3edf@ec2-44-199-22-207.compute-1.amazonaws.com:5432/d910mafk2ua9b8')

session = sessionmaker(engine)

Base = declarative_base(engine)


class Language(Base):
    __tablename__ = 'Languages'

    id = Column(Integer, primary_key=True)
    language = Column(String(250), nullable=False)
    r = relationship('Requests')


class Requests(Base):
    __tablename__ = 'Requests'

    id = Column(Integer, primary_key=True)
    language_id = Column(Integer, ForeignKey('Languages.id'))
    region_id = Column(Integer, ForeignKey('Regions.id'))
    vacancies = Column(Integer)
    date = Column(Date)


class Regions(Base):
    __tablename__ = 'Regions'

    id = Column(Integer, primary_key=True)
    region = Column(String(255), nullable=False)
    r = relationship('Requests')
