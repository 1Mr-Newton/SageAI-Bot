from datetime import datetime
import json
import os
import uuid
from sqlalchemy import (
    Column,
    String,
    DateTime,
    ForeignKey,
    Table,
    UUID,
    Text,
    create_engine,
)
from sqlalchemy.orm import relationship, declarative_base, sessionmaker


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


def generate_uuid():
    return uuid.uuid4()


class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    user_id = Column(String, unique=True)
    current_conv_id = Column(UUID(as_uuid=True))
    conversations = relationship("Conversation", backref="user")
    oauth_providers = relationship("OAuthProvider", backref="user")

    def to_dict(self):
        user_dict = {
            "id": str(self.id),
            "user_id": self.user_id,
            "current_conv_id": (
                str(self.current_conv_id) if str(self.current_conv_id) else None
            ),
            "conversations": [
                conversation.to_dict() for conversation in self.conversations
            ],
            "oauth_providers": [
                oauth_provider.to_dict() for oauth_provider in self.oauth_providers
            ],
        }
        return user_dict


class OAuthProvider(Base):
    __tablename__ = "oauth_providers"
    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    provider = Column(String, nullable=False)
    oauth_scopes = relationship("OAuthScope", backref="oauth_provider")

    def to_dict(self):
        oauth_provider_dict = {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "provider": self.provider,
            "oauth_scopes": [scope.to_dict() for scope in self.oauth_scopes],
        }
        return oauth_provider_dict


class OAuthScope(Base):
    __tablename__ = "oauth_scopes"
    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    provider_id = Column(UUID(as_uuid=True), ForeignKey("oauth_providers.id"))
    scope = Column(String, nullable=False)

    def to_dict(self):
        oauth_scope_dict = {
            "id": str(self.id),
            "provider_id": str(self.provider_id),
            "scope": self.scope,
        }
        return oauth_scope_dict


class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    messages = Column(Text)
    title = Column(String)

    @property
    def messages_data(self):
        return json.loads(str(self.messages))


if not os.path.exists("mydatabase.db"):
    Base.metadata.create_all(engine)

# user = session.query(User).first()
# if user:
#     for conv in user.conversations:
#         print(conv.title)
#     conv = (
#         session.query(Conversation)
#         .filter(Conversation.id == user.current_conv_id)
#         .first()
#     )
#     print(conv.messages_data())
