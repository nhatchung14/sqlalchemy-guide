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

    # Query for all
    query_all = session.query(User).all()
    print("\n===> Table: Users, query for all")
    for inst in query_all:
        print(inst)
    print('')

    # Deleting a user
    calvin = session.query(User).filter_by(name="Calvin").first()
    session.delete(calvin)
    query_all = session.query(User).all()
    print("\n===> Table: Users, after deleting a user Calvin")
    for inst in query_all:
        print(inst)
    print('')

    # Adding another user
    user_false = User(name='Deakin',  fullname='Deakin Drama', nickname='dea')
    session.add(user_false)
    query_all = session.query(User).all()
    print("\n===> Table: Users, after adding a user Deakin")
    for inst in query_all:
        print(inst)
    print('')
    
    # Undoing
    session.rollback()
    query_all = session.query(User).all()
    print("\n===> Table: Users, after rolling back")
    for inst in query_all:
        print(inst)
    print('')

    session.commit()