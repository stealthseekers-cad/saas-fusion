from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# The database URL tells SQLAlchemy how to connect.
# We connect to host 'db' (the service name from docker-compose.yml),
# with user 'user', password 'password', and database 'app_db'.
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@db/app_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
