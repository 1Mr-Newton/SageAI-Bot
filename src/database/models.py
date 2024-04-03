from datetime import datetime
import os
import uuid
from sqlalchemy import (
    Column,
    String,
    DateTime,
    ForeignKey,
    Table,
    UUID,
    create_engine,
)
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from sqlalchemy.sql import func

Base = declarative_base()

engine = create_engine("sqlite:///mydatabase.db", echo=False, future=True)

Session = sessionmaker(bind=engine)
session = Session()

user_oauth_scopes = Table(
    "user_oauth_scopes",
    Base.metadata,
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id")),
    Column("provider", String, nullable=False),
    Column("scope", String, nullable=False),
)


class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String, unique=True)
    current_conv_id = Column(UUID(as_uuid=True))
    conversations = relationship("Conversation", backref="user")
    oauth_providers = relationship("OAuthProvider", backref="user")


class OAuthProvider(Base):
    __tablename__ = "oauth_providers"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    provider = Column(String, nullable=False)
    oauth_scopes = relationship("OAuthScope", backref="oauth_provider")


class OAuthScope(Base):
    __tablename__ = "oauth_scopes"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    provider_id = Column(UUID(as_uuid=True), ForeignKey("oauth_providers.id"))
    scope = Column(String, nullable=False)


class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    messages = relationship(
        "Message", order_by="Message.timestamp", back_populates="conversation"
    )


class Message(Base):
    __tablename__ = "messages"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content = Column(String)
    role = Column(String(50))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id"))
    conversation = relationship("Conversation", back_populates="messages")


if not os.path.exists("mydatabase.db"):
    Base.metadata.create_all(engine)

# """from datetime import datetime
# import os
# import uuid
# from sqlalchemy import Column, String, DateTime, ForeignKey, Table, UUID, create_engine
# from sqlalchemy.orm import relationship, declarative_base, sessionmaker


# Base = declarative_base()

# engine = create_engine("sqlite:///mydatabase.db", echo=False, future=True)

# Session = sessionmaker(bind=engine)
# session = Session()

# user_oauth_scopes = Table(
#     "user_oauth_scopes",
#     Base.metadata,
#     Column("user_id", UUID(as_uuid=True), ForeignKey("users.id")),
#     Column("provider", String, nullable=False),
#     Column("scope", String, nullable=False),
# )


# def generate_uuid():
#     return uuid.uuid4()


# class User(Base):
#     __tablename__ = "users"
#     id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
#     user_id = Column(String, unique=True)
#     current_conv_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id"))
#     conversations = relationship("Conversation", backref="user")
#     oauth_providers = relationship("OAuthProvider", backref="user")

#     def to_dict(self):
#         user_dict = {
#             "id": str(self.id),
#             "user_id": self.user_id,
#             "current_conv_id": (
#                 str(self.current_conv_id) if str(self.current_conv_id) else None
#             ),
#             "conversations": [
#                 conversation.to_dict() for conversation in self.conversations
#             ],
#             "oauth_providers": [
#                 oauth_provider.to_dict() for oauth_provider in self.oauth_providers
#             ],
#         }
#         return user_dict


# class OAuthProvider(Base):
#     __tablename__ = "oauth_providers"
#     id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
#     user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
#     provider = Column(String, nullable=False)
#     oauth_scopes = relationship("OAuthScope", backref="oauth_provider")

#     def to_dict(self):
#         oauth_provider_dict = {
#             "id": str(self.id),
#             "user_id": str(self.user_id),
#             "provider": self.provider,
#             "oauth_scopes": [scope.to_dict() for scope in self.oauth_scopes],
#         }
#         return oauth_provider_dict


# class OAuthScope(Base):
#     __tablename__ = "oauth_scopes"
#     id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
#     provider_id = Column(UUID(as_uuid=True), ForeignKey("oauth_providers.id"))
#     scope = Column(String, nullable=False)

#     def to_dict(self):
#         oauth_scope_dict = {
#             "id": str(self.id),
#             "provider_id": str(self.provider_id),
#             "scope": self.scope,
#         }
#         return oauth_scope_dict


# class Conversation(Base):
#     __tablename__ = "conversations"
#     id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
#     user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
#     messages = relationship(
#         "Message", order_by="Message.timestamp", back_populates="conversation"
#     )

#     def to_dict(self):
#         conversation_dict = {
#             "id": str(self.id),
#             "user_id": str(self.user_id),
#             "messages": [message.to_dict() for message in self.messages],
#         }
#         return conversation_dict


# class Message(Base):
#     __tablename__ = "messages"
#     id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
#     content = Column(String)
#     role = Column(String(50))
#     timestamp = Column(DateTime, index=True, default=datetime.now)
#     conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id"))
#     conversation = relationship("Conversation", back_populates="messages")

#     def to_dict(self):
#         message_dict = {
#             "id": str(self.id),
#             "content": self.content,
#             "role": self.role,
#             "timestamp": self.timestamp.isoformat(),
#             "conversation_id": str(self.conversation_id),
#         }
#         return message_dict


# if not os.path.exists("mydatabase.db"):
#     Base.metadata.create_all(engine)
# """
