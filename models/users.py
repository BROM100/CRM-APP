import sys
from sqlalchemy import Column, Integer, String, ForeignKey, Table, create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker,declarative_base
from .base import Base



#Base = declarative_base()
class Users(Base):
    __tablename__ = "Users"
    ID = Column(Integer, primary_key=True)
    Login = Column(String)
    Password = Column(String)
    First_Name = Column(String)
    Last_Name = Column(String)
    Email = Column(String)
    Type = Column(String)

    orders = relationship("Orders", back_populates="user", lazy='joined')

