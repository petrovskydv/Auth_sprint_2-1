from authlib.integrations.flask_client import OAuth

from src.db.redis_db import redis_conn

oauth = OAuth()

oauth.register(
    name="google",
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        "scope": "openid email profile"
    }
)
oauth.register(
    name='yandex',
    access_token_url='https://oauth.yandex.ru/token',
    authorize_url='https://oauth.yandex.ru/authorize',
    api_base_url='https://login.yandex.ru/info',
    client_kwargs={
        "scope": "login:email login:info"
    }
)


def init_oauth(app):
    oauth.init_app(app)
    oauth.google.framework.cache = redis_conn
    oauth.yandex.framework.cache = redis_conn
