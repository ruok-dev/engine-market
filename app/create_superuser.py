from sqlmodel import Session, select
from app.core.db import engine
from app.models.user import User
from app.core.security import get_password_hash
from app.core.config import settings

def create_superuser():
    with Session(engine) as session:
        # Check if superuser already exists
        statement = select(User).where(User.email == "admin@enginemarket.com")
        existing_user = session.exec(statement).first()
        
        if existing_user:
            print("Superuser already exists.")
            return

        user = User(
            email="admin@enginemarket.com",
            hashed_password=get_password_hash("admin123"),
            full_name="Admin",
            is_active=True,
            is_superuser=True
        )
        session.add(user)
        session.commit()
        print("Superuser created successfully.")

if __name__ == "__main__":
    create_superuser()
