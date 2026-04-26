from sqlmodel import create_engine, SQLModel, Session
from app.core.config import settings

engine = create_engine(settings.sync_database_url)

def init_db():
    # This will be used to create tables if not using migrations
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
