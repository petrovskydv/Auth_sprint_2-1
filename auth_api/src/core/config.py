from pydantic import BaseSettings, Field


# Environment Settings
class MainSettings(BaseSettings):
    class Config:
        env_file_encoding = 'utf-8'
        use_enum_values = True
        env_file = '.env'


class ApiSettings(MainSettings):
    secret_key: str = Field(..., env='SECRET_KEY')
    salt: str = Field(..., env='SALT')
    flask_debug: bool = Field(False, env='FLASK_DEBUG')
    refresh_jwt_token_duration: int = Field(False, env='REFRESH_JWT_TOKEN_DURATION')
    access_jwt_token_duration: int = Field(False, env='ACCESS_JWT_TOKEN_DURATION')
    superuser_role_name: str = Field(False, env='SUPERUSER_ROLE_NAME')


class RedisSettings(MainSettings):
    redis_host: str = Field(..., env='REDIS_HOST')
    redis_port: int = Field(..., env='REDIS_PORT')


class PostgresSettings(MainSettings):
    postgres_user: str = Field(..., env='POSTGRES_USER')
    postgres_password: str = Field(..., env='POSTGRES_PASSWORD')
    postgres_db: str = Field(..., env='POSTGRES_DB')
    postgres_host: str = Field(..., env='POSTGRES_HOST')
    postgres_port: int = Field(..., env='POSTGRES_PORT')

class JaegerSettings(MainSettings):
    agent_host: str = Field(..., env='JAEGER_HOST')
    agent_port: int = Field(..., env='JAEGER_AGENT_PORT')

redis_settings = RedisSettings()
pg_settings = PostgresSettings()
api_settings = ApiSettings()
jaeger_settings = JaegerSettings()

# Flask Configuration
SECRET_KEY = api_settings.secret_key
SECURITY_PASSWORD_SALT = api_settings.salt
JWT_TOKEN_LOCATION = ["headers"]
JWT_ACCESS_TOKEN_EXPIRES = api_settings.access_jwt_token_duration
JWT_REFRESH_TOKEN_EXPIRES = api_settings.refresh_jwt_token_duration
SUPERUSER_ROLE_NAME = api_settings.superuser_role_name
SQLALCHEMY_DATABASE_URI = 'postgresql://{user}:{password}@{host}:{port}/{db}'.format(
        user=pg_settings.postgres_user,
        password=pg_settings.postgres_password,
        host=pg_settings.postgres_host,
        port=pg_settings.postgres_port,
        db=pg_settings.postgres_db,
    )
