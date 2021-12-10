import datetime

from fastapi import HTTPException, Depends
from fastapi import status
from fastapi.security import OAuth2PasswordBearer

from jose import jwt, JWTError
from passlib.hash import bcrypt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from .. import tables
from ..database import get_session
from ..schemas import auth
from ..settings import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/sign-in")


def get_current_user(token: str = Depends(oauth2_scheme)) -> auth.User:
    return AuthService.verify_token(token)


class AuthService:
    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.verify(plain_password, hashed_password)

    @classmethod
    def hash_password(cls, password: str) -> str:
        return bcrypt.hash(password)

    @classmethod
    def verify_token(cls, token: str) -> auth.User:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token=token, key=settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        except JWTError:
            raise exception from None

        user_data = payload.get("user")

        try:
            user = auth.User.parse_obj(user_data)
        except ValidationError:
            raise exception from None

        return user

    @classmethod
    def create_token(cls, user: tables.User) -> auth.Token:
        user_data = auth.User.from_orm(user)

        now = datetime.datetime.utcnow()

        payload = {
            "iat": now,
            "nbf": now,
            "exp": now + datetime.timedelta(seconds=settings.jwt_token_expiration),
            "sub": user_data.id,
            "user": user_data.dict(),
        }
        token = jwt.encode(payload, key=settings.jwt_secret, algorithm=settings.jwt_algorithm)
        return auth.Token(access_token=token)

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def register_new_user(self, user_data: auth.UserCreate) -> auth.Token:
        user = tables.User(
            username=user_data.username,
            surname="",
            description="",
            email=user_data.email,
            password_hash=self.hash_password(user_data.password),
        )
        self.session.add(user)
        self.session.commit()
        return self.create_token(user)

    def authenticate_user(self, username: str, password: str) -> auth.Token:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

        user: tables.User = self.session.query(tables.User).filter(tables.User.username == username).first()
        if not user:
            raise exception

        if not self.verify_password(password, user.password_hash):
            raise exception

        return self.create_token(user)
