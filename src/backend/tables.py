from datetime import datetime
from sqlalchemy import Table, Column, ForeignKey, Integer, String, DateTime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

member_association = Table(
    "member_association",
    Base.metadata,
    Column("chat_id", ForeignKey("backend.id"), primary_key=True),
    Column("user_id", ForeignKey("user.id"), primary_key=True),
)


class Chat(Base):
    __tablename__ = "backend"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    members = relationship("User", secondary=member_association, backref="chats", cascade="all, delete")


class User(Base):
    """
    User Model:
        —
    """

    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    surname = Column(String(length=120), nullable=True)
    description = Column(String(length=255), nullable=True)
    email = Column(String(length=255), unique=True)
    password_hash = Column(String)
    created_at = Column(DateTime, nullable=False, default=datetime.now)


class Message(Base):
    """
    Message Model:
        — id(int)`PK`
        — text(str)
        — created_at(datetime)
        — owner_id(int)`FK`
    """

    __tablename__ = "message"

    id = Column(Integer, primary_key=True, autoincrement=True)
    message_text = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)

    owner_id = Column(Integer, ForeignKey("user.id"), index=True)
    owner = relationship("User", backref="message")

    to_chat_id = Column(Integer, ForeignKey("backend.id"))
    to_chat = relationship("Chat", backref="backend")
