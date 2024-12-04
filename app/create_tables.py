from sqlalchemy import create_engine
from database import Base
from config import settings

engine = create_engine(settings.database_url)

def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")

if __name__ == "__main__":
    create_tables()


