from apiflask import APIBlueprint, abort, pagination_builder
from flask_security.utils import hash_password
from marshmallow.fields import Boolean

from src.api.v1.schemas import UserIn, UserOut, AuthHistoryOut, RoleName, RoleOut, AuthHistoryQuery
from src.services import user as user_service, role as role_service
from src.services.jwt_service import check_role_jwt, auth

users_route = APIBlueprint('users', __name__, )


@users_route.post('/register')
@users_route.input(UserIn)
@users_route.output(UserOut, status_code=201)
def create_user(data):
    user = user_service.get_user(email=data['email'])
    if user:
        abort(400, message='Such email already exists')
    created_user = user_service.create_user_in_db(email=data['email'], password=hash_password(data['password']))
    return created_user


@users_route.patch('/')
@users_route.input(UserIn)
@users_route.output(UserOut, status_code=201)
@users_route.auth_required(auth)
@check_role_jwt('user')
def update_user(data):
    user_by_email = user_service.get_user(email=data['email'])
    if user_by_email and auth.current_user != user_by_email:
        abort(400, message='Such mail already exists')

    updated_user = user_service.update_user_in_db(
        auth.current_user,
        email=data['email'],
        password=hash_password(data['password'])
    )
    return updated_user


@users_route.get('/auth_history')
@users_route.input(AuthHistoryQuery, location='query')
@users_route.output(AuthHistoryOut)
@users_route.auth_required(auth)
@check_role_jwt('user')
def get_auth_history(query):
    pagination = user_service.get_auth_history_by_user_id(auth.current_user.id, query['page'], query['per_page'])
    return {
        'items': pagination.items,
        'pagination': pagination_builder(pagination)
    }


@users_route.post('/<user_id>/roles')
@users_route.input(RoleName)
@users_route.output({'result': Boolean()})
@users_route.auth_required(auth)
@check_role_jwt('admin')
def add_role_to_user(user_id, data):
    user = user_service.get_user_or_404(id=user_id)
    role = role_service.get_role_by_name_or_404(data['name'])
    result = user_service.add_role_to_user(user, role)
    if not result:
        abort(400, message='role already exists')

    return {'result': result}


@users_route.delete('/<user_id>/roles')
@users_route.input(RoleName)
@users_route.output({'result': Boolean()})
@users_route.auth_required(auth)
@check_role_jwt('admin')
def remove_role_from_user(user_id, data):
    user = user_service.get_user_or_404(id=user_id)
    role = role_service.get_role_by_name_or_404(data['name'])
    result = user_service.remove_role_from_user(user, role)
    if not result:
        abort(400, message='User does not have such a role')

    return {'result': result}


@users_route.get('/<user_id>/roles')
@users_route.output(RoleOut(many=True))
@users_route.auth_required(auth)
@check_role_jwt('admin')
def get_user_roles(user_id):
    user = user_service.get_user_or_404(id=user_id)
    return user.roles
