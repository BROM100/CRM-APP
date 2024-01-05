from sqlalchemy import Column, Integer, String, ForeignKey, Table, create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker,declarative_base, relationship
#from .contacts import Contacts
#Base = declarative_base()
from .base import Base
class Customers(Base):
    __tablename__ = "Customers"
    ID = Column(Integer, primary_key=True)
    Name = Column(String)
    Address = Column(String)
    Domain = Column(String)
    IBAN = Column(String)
    Contact_ID = Column(Integer, ForeignKey('Contacts.ID'))
    Orders_count = Column(String)
    Lead_ID = Column(Integer, ForeignKey('Leads.ID'))
    Department = Column(String)

    contact = relationship("Contacts", back_populates="customers", lazy='joined')
    lead = relationship("Leads", back_populates="customer", lazy='joined')