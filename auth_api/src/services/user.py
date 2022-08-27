from datetime import datetime

from src.db.pg_db import db
from src.models.models import User, AuthHistory


def create_user_in_db(**kwargs):
    user = User(**kwargs)
    db.session.add(user)
    db.session.commit()
    return user


def update_user_in_db(user, **kwargs):
    for key, value in kwargs.items():
        setattr(user, key, value)
    db.session.commit()
    return user


def get_user_or_404(**kwargs):
    return User.query.filter_by(**kwargs).first_or_404()


def get_user(**kwargs):
    return User.query.filter_by(**kwargs).first()


def update_history(user_agent, user_id):
    history = AuthHistory.query.filter_by(user_id=user_id, user_agent=user_agent).first()
    if not history:
        history = AuthHistory(user_id=user_id, user_agent=user_agent)
    history.updated_at = datetime.utcnow()
    db.session.add(history)
    db.session.commit()


def get_auth_history_by_user_id(user_id, page, per_page):
    return AuthHistory.query.filter_by(user_id=user_id).paginate(page=page, per_page=per_page)


def add_role_to_user(user, role):
    if role not in user.roles:
        user.roles.append(role)
        db.session.commit()
        return True
    return False


def remove_role_from_user(user, role):
    if role in user.roles:
        user.roles.remove(role)
        db.session.commit()
        return True
    return False
