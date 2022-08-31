from apiflask import APIBlueprint
from apiflask import fields as af_fields
from flask import request, url_for

from src.api.v1.schemas import Token
from src.services import user as user_service, oauth as oauth_service
from src.services.jwt_service import jwt_service

oauth_route = APIBlueprint('oauth', __name__, )


@oauth_route.get('/login/<string:social_name>/')
@oauth_route.output({'url': af_fields.URL()})
def get_redirect_url(social_name):
    redirect_url = url_for('oauth.auth', social_name=social_name, _external=True)
    url = oauth_service.get_social_redirect_url_or_404(redirect_url, social_name)
    return {'url': url}


@oauth_route.get('/auth/<string:social_name>/')
@oauth_route.output(Token)
def auth(social_name):
    user = oauth_service.get_user_from_social(social_name)

    # Обновим историю посещений пользователя
    user_service.update_history(user_agent=request.headers.get('User-Agent'), user_id=user.id)
    return jwt_service.add_new_token_pair(user)
