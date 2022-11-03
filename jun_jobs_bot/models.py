from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from jun_jobs_bot.settings import DB_USERNAME, DB_PASSWORD, \
    HOST, PORT, DATABASE

engine = create_engine(f'postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@'
                       f'{HOST}:{PORT}/{DATABASE}')

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
