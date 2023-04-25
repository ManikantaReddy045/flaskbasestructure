from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, MetaData





engine = create_engine('postgresql://postgres:Mani%4012345@localhost:5432/flask')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
metadata = MetaData()
Base.query = db_session.query_property()

def init_db():
    metadata.create_all(bind=engine)




