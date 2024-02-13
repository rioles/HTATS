from api.v1.endpoints import app_views
from flask_cors import cross_origin
from datetime import timedelta, datetime
from flask import abort, jsonify, make_response, request
from models.role import Role
from models.token_block_list import TokenBlockList
from models.user_role import UserRoles
from services.object_manager_adapter import ObjectManagerAdapter
from services.paginator import Paginator
from models.user import User
from models.login_history import LoginHistory
from datetime import datetime
from flask_jwt_extended import create_access_token, jwt_required, create_refresh_token, get_jwt_identity,get_jwt,decode_token

#import logging
from services.object_manager_interface import ObjectManagerInterface
from services.room_service.room_category_manager.adapter.room_category_adapter import CreateCategoryRoom
from services.user.user_adapter import UserAdapter
from services.user.user_port import UserManagerInterface
#logging.basicConfig(filename='/tmp/userlogin.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
@app_views.route('/user', methods=['POST'], strict_slashes=False)
@cross_origin()
def post_user():
    """create a new category"""
    if not request.get_json():
        return make_response(jsonify(
            {'status': '401', 'message': 'The request data is empty'}), 400)
    obj:ObjectManagerInterface = ObjectManagerAdapter()
    user = obj.find_object_by(User, **{"email":request.get_json()["email"]})
    #logging.debug("user.. %s", user)
    if user is not None:
        return make_response(jsonify(
            {'status': '409', 'message': f'user with email {user.email} already exists'}), 409)
    user_manager:UserManagerInterface = UserAdapter()    
    user_dict = user_manager.add_object(User, **request.get_json())
    return make_response(jsonify(user_dict), 201)


@app_views.route('/userss', methods=['GET'], strict_slashes=False)
@cross_origin()
def get_user():
    """create a new category"""
    if not request.get_json():
        return make_response(jsonify(
            {'status': '404', 'message': 'The request data is empty'}), 400)
    print(request.get_json())
    obj:ObjectManagerInterface = ObjectManagerAdapter()
    user = obj.find_object_by(User, **{"email":request.get_json()["email"]})
    role = None
    user_objec = {}
    if user is None:
        return make_response(jsonify(
            {'status': '400', 'message': 'incorrect password or email'}), 400)
    else:       
        user_role = obj.find_object_by(UserRoles,**{"user_id":user.id})
        role = obj.find_object_by(Role,**{"id":user_role.role_id})
        user_objec["role"] = role.to_dict()
        user_objec["user"] = user.to_dict()
    return make_response(jsonify(user_objec), 200)

@app_views.route('/login', methods=['POST'], strict_slashes=False)
@cross_origin()
def login_handler():
    """create a new category"""
    if not request.get_json():
        return make_response(jsonify(
            {'status': '401', 'message': 'The request data is empty'}), 400)
    user_manager:UserManagerInterface = UserAdapter() 
    user = user_manager.get_user_log(**request.get_json())
    obj:ObjectManagerInterface = ObjectManagerAdapter()
    print(user)
    if user is not None:
        access_token = create_access_token(identity=user["user"]["email"])
        refresh_token = create_refresh_token(identity=user["user"]["email"])
        decoded_token = decode_token(access_token)
        print("acess tokii",decoded_token)
        response_data = {'access_token': access_token, 'refresh_token': refresh_token, 'user': user}
        connexion_metadata = {"user_id":user["user"]["id"], "login_timestamp": datetime.utcnow()}
        obj.add_object(LoginHistory, **connexion_metadata)
        return make_response(jsonify(response_data), 200)
    else:
        return make_response(jsonify({'status': '404', 'message': f'no user with email {request.get_json()["email"]} or password  exists'}), 400)


@app_views.route('/users', methods=['GET'], strict_slashes=False)
@cross_origin()
def get_users():
    """list of users"""
    obj:UserManagerInterface = UserAdapter()
    users = obj.find_all_users_entities()
    print(users)
    page_obj = Paginator(users)
    page = request.args.get('page', default=1, type=int)  # Get the page parameter from the request query string
    per_page = request.args.get('per_page', default=10, type=int)  # Get the per_page parameter from the request query string
    result = page_obj.get_hyper(page, per_page)
    return jsonify(result)

@app_views.route('/user', methods=['PUT'], strict_slashes=False)
@cross_origin()
def put_user():
    """list of users"""
    if not request.get_json():
        return make_response(jsonify(
            {'status': '400', 'message': 'The request data is empty'}), 400)
    obj:ObjectManagerInterface = ObjectManagerAdapter()
    user = obj.find_object_by(User, **{"email":request.get_json()["email"]})
    #logging.debug("user.. %s", user)
    if user is not None:
        return make_response(jsonify(
            {'status': '409', 'message': f'user with email {user.email} already exists'}), 409)
    obj:UserManagerInterface = UserAdapter()
    user = obj.update_user(**request.get_json())
    return jsonify(user), 200

@app_views.route('/refresh', methods=['GET'], strict_slashes=False)
@cross_origin()
@jwt_required()
def refresh_access():
    """refresh token for users"""
    identity = get_jwt_identity()
    new_access_token = create_access_token(identity=identity)
    user_manager:UserManagerInterface = UserAdapter() 
    user = user_manager.get_user_log(**{"email":identity})
    response_data = {'access_token': new_access_token, 'user': user}
    return make_response(jsonify(response_data), 200)


   
    
@app_views.route('/logout', methods=['POST'], strict_slashes=False)
@cross_origin()
@jwt_required()
def revoke_token():
    jwt = get_jwt()
    jti = jwt["jti"]
    print("jti",jti)
    jwt_data = {"jti":jti}
    obj: ObjectManagerInterface = ObjectManagerAdapter()
    token_revok = obj.add_object(TokenBlockList, **jwt_data)
    user_manager:UserManagerInterface = UserAdapter()
    user = user_manager.get_user_logout(**request.get_json())
    connexion_metadata = {"logout_timestamp": datetime.utcnow()}
    obj.update_object_in_storage(LoginHistory, user["login_history"]["id"], **connexion_metadata)
    return make_response(jsonify(token_revok.to_dict()), 201)

@app_views.route('/whoami', methods=['GET'], strict_slashes=False)
@cross_origin()
@jwt_required()
def whoami():
    return make_response(jsonify({"message":"yako"}))

