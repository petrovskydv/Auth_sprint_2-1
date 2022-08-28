import click
from apiflask import APIFlask
from flask import request
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_security import Security, SQLAlchemyUserDatastore
from flask_security.utils import hash_password
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.instrumentation.flask import FlaskInstrumentor

from src.api.v1.auth import auth_route
from src.api.v1.roles import roles_route
from src.api.v1.users import users_route
from src.core.config import api_settings
from src.db.pg_db import init_db, db
from src.db.redis_db import redis_service
from src.models.models import User, Role
from src.services.role import create_role_in_db, get_role_by_name
from src.services.user import create_user_in_db, add_role_to_user, get_user
from src.core.tracers import configure_tracer


def create_app(config_path):
    app = APIFlask(__name__, docs_path='/')
    app.config.from_pyfile(config_path)

    init_db(app)
    SQLAlchemyInstrumentor().instrument(engine=db.engine)
    jwt = JWTManager(app)

    # from src.db.pg_db import db
    # from src.models.models import User, Role
    migrate = Migrate(app, db)
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)

    @jwt.token_in_blocklist_loader
    def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
        """Колбэк, который проверяет, находится ли токен среди отозванных токенов в Рэдис. Если функция возвращает True,
        то эндпоинты, защищенные jwt_required(), возвратят сообщение 'Token has been revoked'
        """
        jti = jwt_payload["jti"]
        token_in_redis = redis_service.get(jti)

        return token_in_redis is not None

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        """
        Callback для поиска пользователя
        """
        identity = jwt_data["sub"]
        user = get_user(id=identity)
        return user

    api_v1 = '/auth/api/v1'
    app.register_blueprint(roles_route, url_prefix=f'{api_v1}/roles')
    app.register_blueprint(auth_route, url_prefix=f'{api_v1}/auth')
    app.register_blueprint(users_route, url_prefix=f'{api_v1}/users')

    return app


app = create_app('src/core/config.py')


@app.before_request
def before_request():
    request_id = request.headers.get('X-Request-Id')
    if not request_id:
        raise RuntimeError('request id is required')


# Конфигурируем и добавляем трейсер
configure_tracer()
FlaskInstrumentor().instrument_app(app)


@app.cli.command("create-superuser")
@click.argument("email")
@click.argument("password")
def create_superuser(email: str, password: str) -> None:
    """Консольная команда для добавления суперюзера"""
    # Проверим существование Роли и добавим при необходимости
    if not get_role_by_name(api_settings.superuser_role_name):
        create_role_in_db(
            {
                'name': api_settings.superuser_role_name,
                'description': "This Role exists only for admins"
            }
        )

    # Добавим Юзера
    if not get_user(email=email):
        create_user_in_db(email=email, password=hash_password(password))

    # Добавим Юзеру Админскую Роль
    created_user = get_user(email=email)
    superuser_role = get_role_by_name(api_settings.superuser_role_name)
    add_role_to_user(created_user, superuser_role)

    return None


if __name__ == '__main__':
    app.run(debug=api_settings.flask_debug)
