#!/usr/bin/python3
"""A class for SQLAlchemy database storage."""
import os
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class DBStorage:
    """Database storage class for SQLAlchemy."""

    __engine = None
    __session = None

    def __init__(self):
        """Initialize the DBStorage class."""
        user = os.getenv("HBNB_MYSQL_USER")
        passwd = os.getenv("HBNB_MYSQL_PWD")
        db = os.getenv("HBNB_MYSQL_DB")
        host = os.getenv("HBNB_MYSQL_HOST")
        env = os.getenv("HBNB_ENV")

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(user, passwd, host, db),
                                      pool_pre_ping=True)

        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Return a dictionary of objects."""
        obj_dict = {}

        if cls:
            if isinstance(cls, str):
                cls = eval(cls)
            query = self.__session.query(cls)
            for obj in query:
                key = "{}.{}".format(type(obj).__name__, obj.id)
                obj_dict[key] = obj
        else:
            model_classes = [State, City, User, Place, Review, Amenity]
            for model_class in model_classes:
                query = self.__session.query(model_class)
                for obj in query:
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    obj_dict[key] = obj

        return obj_dict

    def new(self, obj):
        """Add a new object to the session."""
        self.__session.add(obj)

    def save(self):
        """Commit changes to the session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete an object from the session."""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Configure and reload the session."""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Close the session."""
        self.__session.close()
