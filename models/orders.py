from sqlalchemy import Column, Integer, String, ForeignKey, Table, create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker, declarative_base, relationship
# from .contacts import Contacts
# Base = declarative_base()
from .base import Base


class Orders(Base):
    __tablename__ = "Orders"
    ID = Column(Integer, primary_key=True)
    CustomerID = Column(Integer, ForeignKey('Customers.ID'))
    ProductID = Column(Integer, ForeignKey('Products.ID'))
    Date = Column(String)
    UserID = Column(Integer, ForeignKey('Users.ID'))
    Amount = Column(Integer)
    Discount = Column(Integer)
    Total = Column(Integer)
    user = relationship("Users", back_populates="orders", lazy='joined')
    customer = relationship("Customers", back_populates="orders", lazy='joined')
    product = relationship("Products", back_populates="orders", lazy='joined')
