# Imports
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

# For defining our own classes which will be mapped to database tables
Base = declarative_base()

from sqlalchemy import Column, Date, Integer, String
from sqlalchemy import Sequence

# Database credential constants
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String)
    fullname = Column(String)
    nickname = Column(String)

    def __repr__(self):
       return "<User(name='%s', fullname='%s', nickname='%s')>" % (
                            self.name, self.fullname, self.nickname)

# Getting connection
def get_connection(dialect, db_path):
    return create_engine(
        url="{0}:///{1}".format(dialect, db_path),
        echo=True        # to generate activity log
    )

from sqlalchemy.orm import sessionmaker

# Driver section
if __name__ == '__main__':
    engine = get_connection('sqlite', 'user.db')
    Base.metadata.create_all(engine)

    # The Session is a workspace for your objects, local to a particular database connection
    Session = sessionmaker(bind=engine)
    session = Session() 

    # Defining some users to be added
    users = [
        User(name='Alice',  fullname='Alice Algebra', nickname='al'),
        User(name='Bobby',  fullname='Bobby Bongo', nickname='bob'),
        User(name='Calvin', fullname='Calvin Chemistry', nickname='cal'),
    ]

    # Adding alice
    session.add(users[0])
    query_all = session.query(User).all()
    print("\n===> Table: Users, after adding Alice")
    for inst in query_all:
        print(inst)
    print('')

    # Adding others
    session.add_all(users[1:])
    query_all = session.query(User).all()
    print("\n===> Table: Users, after adding others")
    for inst in query_all:
        print(inst)
    print('')

    # Query for Bobby specifically from Users, but by id
    query_all = session.query(User).filter_by(id=2).all()
    print("\n===> Query for Bobby specifically from Users by id=2")
    for inst in query_all:
        print(inst)
    print('')

    # Export the session to .db
    session.commit()
