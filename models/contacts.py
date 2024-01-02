from sqlalchemy import Column, Integer, String, ForeignKey, Table, create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker,declarative_base, relationship
#from .customers import Customers
from .base import Base
#Base = declarative_base()

class Contacts(Base):
    __tablename__ = "Contacts"
    ID = Column(Integer, primary_key=True)
    First_name = Column(String)
    Last_name = Column(String)
    Email = Column(String)
    Phone = Column(String)
    Gender = Column(String)
    Do_not_call = Column(Integer)

    customers = relationship("Customers", back_populates="contact", lazy='joined')