from sqlalchemy import Column, Integer, String, ForeignKey, Table, create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker,declarative_base

Base = declarative_base()

class Customers(Base):
    __tablename__ = "Customers"
    ID = Column(Integer, primary_key=True)
    Name = Column(String)
    Address = Column(String)
    Domain = Column(String)
    IBAN = Column(String)
    Contact_ID = Column(Integer)
    Orders_count = Column(String)
    Lead_ID = Column(Integer)
    Department = Column(String)