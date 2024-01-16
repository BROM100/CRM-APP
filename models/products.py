from sqlalchemy import Column, Integer, String, ForeignKey, Table, create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker,declarative_base, relationship
#from .contacts import Contacts
#Base = declarative_base()
from .base import Base

class Products(Base):
    __tablename__ = "Products"
    ID = Column(Integer, primary_key=True)
    Name = Column(String)
    Price = Column(Integer)
    SerialNumber = Column(String)


    orders = relationship("Orders", back_populates="product", lazy='joined')
    