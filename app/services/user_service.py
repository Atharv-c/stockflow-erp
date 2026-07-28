from sqlalchemy.orm import Session

from app.core.jwt import create_access_token
from app.core.security import hash_password, verify_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import TokenResponse, UserLogin, UserRegister


class UserService:
    """
    Business logic for user management and authentication.
    """

    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def register(self, data: UserRegister) -> User:
        """
        Register a new user.
        """
        existing_user = self.repository.get_by_email(data.email)

        if existing_user:
            raise ValueError("Email is already registered.")

        user = User(
            full_name=data.full_name,
            email=data.email,
            password_hash=hash_password(data.password),
        )

        return self.repository.create(user)

    def login(self, data: UserLogin) -> TokenResponse:
        """
        Authenticate a user and generate a JWT token.
        """
        user = self.repository.get_by_email(data.email)

        if not user:
            raise ValueError("Invalid email or password.")

        if not verify_password(data.password, user.password_hash):
            raise ValueError("Invalid email or password.")

        token = create_access_token(str(user.id))

        return TokenResponse(
            access_token=token,
        )