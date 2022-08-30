from apiflask import APIBlueprint, exceptions
from authlib.integrations.base_client import OAuthError
from flask import url_for, session, request

from src.services.oauth import oauth

oauth_route = APIBlueprint('oauth', __name__, )


@oauth_route.get('/login/<string:name>')
# @oauth_route.output(RoleOut(many=True))
# @oauth_route.auth_required(auth)
# @check_role_jwt('admin')
def get_redirect_url(name):
    client = oauth.create_client(name)

    if not client:
        raise exceptions.HTTPError

    # redirect_url = url_for('oauth.auth', name=name, _external=True)
    redirect_url = f'https://6b37-79-165-97-187.ngrok.io/auth/api/v1/oauth/auth/{name}/'

    # client.authorize_redirect(redirect_url)
    oauth_url = client.create_authorization_url(redirect_url)['url']
    rv = client.create_authorization_url(redirect_url, response_type='token')
    client.save_authorize_data(redirect_uri=redirect_url, **rv)
    exemple = 'https://accounts.google.com/o/oauth2/v2/auth/oauthchooseaccount?response_type=code&client_id=71795016849-a2pthr10bjbbbcp610llfolqp1j2vqfi.apps.googleusercontent.com&redirect_uri=https%3A%2F%2F090f-79-165-97-187.ngrok.io%2Fauth%2Fgoogle%2F&scope=openid%20email%20profile&state=evx4JJSnYVyqzDenJdt8pdhLkod2Zu&nonce=uIYJEqszAH2EDqB2D1hs&flowName=GeneralOAuthFlow'

    from urllib.parse import urlparse, urlunparse, urlencode, unquote
    res = urlparse(oauth_url)
    print(f'{oauth_url=}')
    print(f'{rv["url"]=}')
    # print(unquote(oauth_url))

    # assert oauth_url==exemple
    # print(oauth_url)
    return rv


@oauth_route.get('/auth/<string:name>/')
# @oauth_route.output(RoleOut(many=True))
# @oauth_route.auth_required(auth)
# @check_role_jwt('admin')
def auth(name):
    print('dkfkdjnbdkkkkkkkkkkkkkkdlfbnsndbs')
    client = oauth.create_client(name)

    if not client:
        raise exceptions.HTTPError

    print(request.args.get('state'), session.get('_google_authlib_state_'))
    token = authorize_access_token(client)
    user_info = token.get("userinfo")

    return user_info


def authorize_access_token(client):
    """Fetch access token in one step.

    :return: A token dict.
    """
    if request.method == 'GET':
        error = request.args.get('error')
        if error:
            description = request.args.get('error_description')
            raise OAuthError(error=error, description=description)

        params = {
            'code': request.args['code'],
            'state': request.args.get('state'),
        }
    else:
        params = {
            'code': request.form['code'],
            'state': request.form.get('state'),
        }

    state_data = client.framework.get_state_data(session, params.get('state'))
    # client.framework.clear_state_data(session, params.get('state'))
    # params = _format_state_params(state_data, params)
    # token = client.fetch_access_token(**params, )
    # userinfo = client.parse_id_token(token, nonce=state_data['nonce'])

    # if 'id_token' in token and 'nonce' in state_data:
    #     userinfo = self.parse_id_token(token, nonce=state_data['nonce'])
    #     token['userinfo'] = userinfo
    return state_data


def _format_state_params(state_data, params):
    code_verifier = state_data.get('code_verifier')
    if code_verifier:
        params['code_verifier'] = code_verifier

    redirect_uri = state_data.get('redirect_uri')
    if redirect_uri:
        params['redirect_uri'] = redirect_uri
    return params
