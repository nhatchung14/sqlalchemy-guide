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

# 1-N relationship
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Email(Base):
    __tablename__ = 'emails'

    id = Column(Integer, Sequence('email_id_seq'), primary_key=True)
    email_name = Column(String, nullable=False)
    domain_name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship("User", back_populates="email") # Email refering to User class by attribute 'user', and User by 'email'

    def __repr__(self):
        return "<Email(email_address='%s')>" % (self.email_name + '@' + self.domain_name)

User.email = relationship("Email", back_populates="user") # User refering to Email class by attribute 'email', and Email by 'user'

# N-N relationship
from sqlalchemy import Table, Text

# - let assume a 'User' can have many 'Role's, and a 'Role' accommodates many 'User's
class Role(Base):
    __tablename__ = 'roles'

    name = Column(String, primary_key=True, nullable=False)
    access_lvl = Column(Integer, nullable=False)
    desc = Column(Text)

    def __repr__(self):
        return "<Role(name='%s', access_lvl='%d', description='%r')>" % (self.name, self.access_lvl, self.desc)

# - we need an association table
user_roles = Table('user_roles', Base.metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('role_id', ForeignKey('roles.name'), primary_key=True)
)

# - defining the many-to-many relationship 
User.role = relationship("Role", 
                         secondary=user_roles, 
                         back_populates="user")
Role.user = relationship("User", 
                         secondary=user_roles, 
                         back_populates="role")

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

    # Query for all users
    query_all = session.query(User).all()
    print("\n===> Table: Users, query for all")
    for inst in query_all:
        print(inst)
    print('')

    # Query for all emails
    query_all = session.query(Email).all()
    print("\n===> Table: Emails, query for all")
    for inst in query_all:
        print(inst)
    print('')

    # Query for all roles
    query_all = session.query(Role).all()
    print("\n===> Table: Roles, query for all")
    for inst in query_all:
        print(inst)
    print('')
    
    # Query for all at the association table
    query_all = session.query(user_roles).all()
    print("\n===> Table: user_roles, query for all")
    for inst in query_all:
        print('<user_role(user_id='+str(inst.user_id)+', role_id='+inst.role_id+')>')
    print('')
    