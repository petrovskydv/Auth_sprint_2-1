import uuid
from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import DateTime, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID

from src.db.pg_db import db

users_roles = db.Table(
    'users_roles',
    db.Column('user_id', UUID(as_uuid=True), db.ForeignKey('users.id')),
    db.Column('role_id', UUID(as_uuid=True), db.ForeignKey('roles.id'))
)


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String, nullable=True)

    def __repr__(self):
        return f'<Role {self.name}>'


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String(255), unique=True)
    roles = db.relationship('Role', secondary=users_roles, backref='users')

    def __repr__(self):
        return f'<User {self.email}>'


class AuthHistory(db.Model):
    __table_args__ = (UniqueConstraint('user_id', 'user_agent', name='_user_id_agent'),
                      )

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    user_agent = db.Column(db.String(255), nullable=False)
    updated_at = db.Column(DateTime(timezone=True), default=datetime.utcnow)


class Token(BaseModel):
    """Модель токена"""
    token: str
    token_type: str
