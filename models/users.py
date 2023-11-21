import sys
from sqlalchemy import Column, Integer, String, ForeignKey, Table, create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker,declarative_base




Base = declarative_base()
class Users(Base):
    __tablename__ = "Users"
    ID = Column(Integer, primary_key=True)
    Login = Column(String)
    Password = Column(String)


