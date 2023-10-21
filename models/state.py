#!/usr/bin/python3
"""State Module for HBNB project"""
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey
from os import getenv
from models.city import City


class State(BaseModel, Base):
    """State Module for HBNB project
    Attributes:
        name: input name
    """

    if getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def cities(self):
            """
            Get the list of City objects associated with this state
            """
            cities = models.storage.all(City)
            return [city for city in cities.values()
                    if city.state_id == self.id]

    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship("City", cascade='all, delete, delete-orphan',
                          backref="state")
