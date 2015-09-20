'''
this file sets up teh database using SQLAlchemy
Created restaurant and menu_item table.
Executing this file creates empty manuapp.db in current directory
Using SQLAlchemy , creating a database is similar to creating objects in python

Creating a database with SQLAlchemy has four major components
1. Configuration - imports all necessary module, sets all dependencies and binds code to SQLAlchemy engine
2. Class - class code is used to represent data in python
3. Table - Table that represents the specific tables in our database
4. Mapper - Mapper connects the column to the class it represents


executing this file creates menuapp db

'''

# configuration

import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


# creates Base class that class code will inherit
# it will make classes make special SQLAlchemy classes that corresponds to tables in database

Base = declarative_base()

class Restaurant(Base):
    # table name
    __tablename__ = 'restaurant'

    # mappers
    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable = False)

    @property
    def serialize(self):
        return {
            'restaurant_name' : self.id,
        }

class MenuItem(Base):
    # table name
    __tablename__ = "menu_item"

    # mappers
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(250))
    price = Column(String(8))
    course = Column(String(250))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)

    @property
    def serialize(self):
        # returns object data in easily serializeable format
        return {
            'name' : self.name,
            'description' : self.description,
            'id' : self.id,
            'price' : self.price,
            'course' : self.course,
        }

# instance of create_engine class and points to the database
engine = create_engine('sqlite:///menuapp.db')

# would add classes as tables in the database
Base.metadata.create_all(engine)



