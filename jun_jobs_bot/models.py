from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from jun_jobs_bot.settings import PATH_TO_BASE


engine = create_engine(f'sqlite:///{PATH_TO_BASE}', echo=True)

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
    vacancies = Column(Integer)
    date = Column(Date)
