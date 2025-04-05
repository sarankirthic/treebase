from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Config import config

DATABASE_URL = config.DATABASE

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
