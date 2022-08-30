from authlib.integrations.flask_client import OAuth

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

)


def init_oauth(app):
    oauth.init_app(app)
