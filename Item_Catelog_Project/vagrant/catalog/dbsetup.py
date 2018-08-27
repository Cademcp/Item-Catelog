import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Category(Base):
    __tablename__ = 'category'
    # Define columns for the table Category
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):

        return {
            'name': self.name,
            'id': self.id
        }


class Item(Base):
    __tablename__ = 'item'
    # Define columns for the table Item
    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    description = Column(String(250))
    category = Column(String(250), ForeignKey('category.name'))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    # Property used for creating JSON endpoint
    @property
    def serialize(self):

        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'category': self.category
        }

engine = create_engine('sqlite:///item_catelog.db')
 
Base.metadata.create_all(engine)
