from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# The database URL tells SQLAlchemy how to connect.
# We are connecting to a postgresql database named 'app_db' with user 'user' and password 'password'
# at the host 'db' (which is the service name from our docker-compose.yml).
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@db/app_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
