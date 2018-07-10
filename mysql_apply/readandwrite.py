# http://techspot.zzzeek.org/2012/01/11/django-style-database-routers-in-sqlalchemy/

# 1. Imports
from sqlalchemy import Column, Integer, String, MetaData, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
import random
import shutil

# 2. Registry of engines.
engines = {
    'leader': create_engine(
        'sqlite:///leader.db',
        logging_name='leader', echo=True),
    'other': create_engine(
        'sqlite:///other.db',
        logging_name='other', echo=True),
    'follower1': create_engine(
        'sqlite:///follower1.db',
        logging_name='follower1', echo=True),
    'follower2': create_engine(
        'sqlite:///follower2.db',
        logging_name='follower2', echo=True),
}

# 3. Our special Session class that handles custom engine routing
# as well as a generative "using_bind()" method.


class RoutingSession(Session):

    def get_bind(self, mapper=None, clause=None):
        if self._name:
            return engines[self._name]
        elif mapper and issubclass(mapper.class_, OtherBase):
            return engines['other']
        elif self._flushing:
            return engines['leader']
        else:
            return engines[
                random.choice(['follower1', 'follower2'])
            ]

    _name = None

    def using_bind(self, name):
        s = RoutingSession()
        vars(s).update(vars(self))
        s._name = name
        return s


# 4. A Base class that sets up some demonstration columns
# for us.

class Base(object):
    id = Column(Integer, primary_key=True)
    data = Column(String(50))

    def __repr__(self):
        return "%s(id=%r, data=%r)" % (
            self.__class__.__name__,
            self.id, self.data
        )

Base = declarative_base(cls=Base)

# 5. Define two bases to distinguish between the "leader/follower"
# setup and the "other" setup.


class DefaultBase(Base):
    __abstract__ = True
    metadata = MetaData()


class OtherBase(Base):
    __abstract__ = True
    metadata = MetaData()

# 6. Three sample model classes.


class Model1(DefaultBase):
    __tablename__ = 'model1'


class Model2(DefaultBase):
    __tablename__ = 'model2'


class Model3(OtherBase):
    __tablename__ = 'model3'

# 7. Erase the existing databases if they exist, this
# is just to make re-running the example more predictable.
import os
for db in 'leader.db', 'follower1.db', 'follower2.db', 'other.db':
    if os.path.exists(db):
        os.remove(db)

# 8a. Create tables - first in the leader/follower...
for eng in 'leader', 'follower1', 'follower2':
    DefaultBase.metadata.create_all(engines[eng])

# 8b. then in "other"...
OtherBase.metadata.create_all(engines['other'])

# 9. Set up the Session
Session = scoped_session(sessionmaker(autocommit=True, class_=RoutingSession))

# 10. then let's use it
s = Session()

with s.begin():
    # 11. Writes go to "leader"....
    s.add_all([
        Model1(data='m1_a'),
        Model2(data='m2_a'),
        Model1(data='m1_b'),
        Model2(data='m2_b'),
        Model3(data='m3_a'),
        Model3(data='m3_b'),
    ])

# 12. Pretend we're using a more substantial database backend
# and "leader' is replicating to "follower1", "follower2"
##### PRETEND PRETEND PRETEND ######
shutil.copy("leader.db", "follower1.db")
shutil.copy("leader.db", "follower2.db")
##### END PRETEND END PRETEND END PRETEND ######

# 13. Queries now hit either "follower1" or "follower2"
print(s.query(Model1).all())
print(s.query(Model2).all())
print(s.query(Model3).all())

# 14. A close() call will rollback the transactional context on any
# engines present.
s.close()

# 15. Use our "using_bind()" method to query a distinct database
m1 = Session().using_bind("leader").query(Model1).first()
assert m1 in Session()