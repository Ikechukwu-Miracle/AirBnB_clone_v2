#!/usr/bin/python3
"""Defines a new class for SQLAlchemy"""
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from os import getenv
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import (create_engine)
from sqlalchemy.ext.declarative import declarative_base


class DBStorage:
    """Class for database storage"""
    __engine = None
    __session = None

    def __init__(self):
        user = getenv("HBNB_MYSQL_USER")
        password = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        dbase = getenv("HBNB_MYSQL_DB")
        env = getenv("HBNB_ENV")

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                        .format(user, password, host, dbase),
                                        pool_pre_ping=True)

        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returns a dictionary"""
        dictionary = {}
        if cls:
            if type(cls) is str:
                cls = eval(cls)
            query_res = self.__session.query(cls)

            for ele in query_res:
                key = "{}.{}".format(type(ele).__name__, elem.id)
                dictionary[key] = ele
        else:
            classes = [State, City, User, Place, Review, Amenity]
            for cla in classes:
                query_res = self.__session.query(cla)
                for ele in query_res:
                    key = "{}.{}".format(type(ele).__name__, elem.id)
                    dictionary[key] = ele
        return dictionary

    def new(self, obj):
        """add a new element in the table"""
        self.__session.add(obj)

    def save(self):
        """save changes"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete an element in the table"""
        if obj:
            self.session.delete(obj)

    def reload(self):
        """ configures the database"""
        Base.metadata.create_all(self.__engine)
        ses = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(ses)
        self.__session = Session()

    def close(self):
        """closes the session"""
        self.__session.close()
