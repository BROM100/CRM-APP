from sqlalchemy import Column, Integer, String, ForeignKey, Table, create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker,declarative_base, relationship
#from .contacts import Contacts
#Base = declarative_base()
from .base import Base


class Leads(Base):
    __tablename__ = "Leads"
    ID = Column(Integer, primary_key=True)
    Name = Column(String)
    Email = Column(String)
    StockSector = Column(String)
    Phone = Column(String)
    Source = Column(String)
    Status = Column(String)


    customer = relationship("Customers", back_populates="lead", lazy='joined')
    #customer = relationship("Customers", back_populates="leads", foreign_keys="Customers.Lead_ID", lazy='joined')