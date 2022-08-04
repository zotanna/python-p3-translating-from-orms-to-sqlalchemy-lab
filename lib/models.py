#!/usr/bin/env python3

from sqlalchemy import (PrimaryKeyConstraint, Column, String, Integer)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Dog(Base):
    __tablename__ = 'dogs'
    __table_args__ = (PrimaryKeyConstraint('dog_id'),)

    dog_id = Column(Integer())
    dog_name = Column(String())
    dog_breed = Column(String())
