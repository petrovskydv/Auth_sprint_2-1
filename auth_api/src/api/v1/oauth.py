import requests
from apiflask import APIBlueprint, exceptions

from src.services.oauth import oauth

oauth_route = APIBlueprint('oauth', __name__, )


@oauth_route.get('/login/<string:name>')
# @oauth_route.output(RoleOut(many=True))
# @oauth_route.auth_required(auth)
# @check_role_jwt('admin')
def get_redirect_url(name):
    # current_app
    client = oauth.create_client(name)

    if not client:
        raise exceptions.HTTPError

    # redirect_url = url_for('oauth.auth', name=name, _external=True)
    redirect_url = f'https://0638-134-0-108-254.ngrok.io/auth/api/v1/oauth/auth/{name}/'

    rv = client.create_authorization_url(redirect_url)
    client.save_authorize_data(redirect_uri=redirect_url, **rv)
    print(f'{rv=}')
    return rv


@oauth_route.get('/auth/<string:name>/')
# @oauth_route.output(RoleOut(many=True))
# @oauth_route.auth_required(auth)
# @check_role_jwt('admin')
def auth(name):
    client = oauth.create_client(name)

    if not client:
        raise exceptions.HTTPError

    token = client.authorize_access_token()

    print(f'{token=}')
    if name == 'yandex':
        headers = {'Authorization': f'Bearer {client.token["access_token"]}'}
        params = {
            'format': 'json',
        }
        response = requests.get(client.api_base_url, headers=headers, params=params)
        response.raise_for_status()
        user = response.json()
    else:
        user = token.get("userinfo")
    print(f'{user}')
    return user
