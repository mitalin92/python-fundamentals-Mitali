from sqlalchemy.orm import sessionmaker
from db_engine import ENGINE

SessionLocal = sessionmaker(bind=ENGINE, autoflush=False, autocommit=False)
