from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    """
    Repository for User database operations.
    """

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> Optional[User]:
        """
        Get a user by ID.
        """
        stmt = select(User).where(User.id == user_id)
        return self.db.scalar(stmt)

    def get_by_email(self, email: str) -> Optional[User]:
        """
        Get a user by email.
        """
        stmt = select(User).where(User.email == email)
        return self.db.scalar(stmt)

    def create(self, user: User) -> User:
        """
        Create a new user.
        """
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user: User) -> User:
        """
        Update an existing user.
        """
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user: User) -> None:
        """
        Delete a user.
        """
        self.db.delete(user)
        self.db.commit()

    def list_all(self) -> list[User]:
        """
        Return all users ordered by ID.
        """
        stmt = select(User).order_by(User.id)
        return list(self.db.scalars(stmt).all())