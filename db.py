from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


def get_engine(path='sqlite:///sample.db'):
    return create_engine(path)


def create_all():
    Base.metadata.create_all(get_engine())


Base = declarative_base()
Session = sessionmaker(bind=get_engine())
session = Session()


if __name__ == '__main__':
    create_all()
