from sqlalchemy import create_engine, Column, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Currency(Base):
    """
    A class representing a currency exchange rate.

    Attributes:
        datetime (DateTime): The datetime when the exchange rate was recorded.
        exchange_rate (Float): The exchange rate value.
    """

    __tablename__ = 'currency'

    datetime = Column(DateTime, primary_key=True)
    exchange_rate = Column(Float)


engine = create_engine('sqlite:///db.sqlite3', echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
