from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# Define CVE Table
class CVE(Base):
    __tablename__ = "cve"
    id = Column(Integer, primary_key=True)
    cve_id = Column(String, unique=True, nullable=False)
    description = Column(String)
    published_date = Column(DateTime)
    last_modified_date = Column(DateTime)
    base_score = Column(String)

# Database connection
DATABASE_URL = "sqlite:///cve_data.db"  # SQLite for simplicity
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)
