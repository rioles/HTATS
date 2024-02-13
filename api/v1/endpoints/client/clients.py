from api.v1.endpoints import app_views
from flask_cors import cross_origin
from flask import abort, jsonify, make_response, request
from models.room import Room
from services.customer.adapter.customer_adapter import CustomerAdapter
from services.customer.port.customer_port import CustormPort
from services.object_manager_adapter import ObjectManagerAdapter
from services.paginator import Paginator
from services.room_service.room.port.room_port import RoomPort
from services.room_service.room.adapter.create_room_adapter import AddRoom
from models.customer import Customer
from models.customer_type import CustormerType
from flask_jwt_extended import  jwt_required, verify_jwt_in_request
from flask_jwt_extended.exceptions import JWTExtendedException


from services.object_manager_interface import ObjectManagerInterface
from services.room_service.room_category_manager.adapter.room_category_adapter import CreateCategoryRoom

@app_views.errorhandler(JWTExtendedException)
def handle_jwt_error(e):
    return jsonify({'message': 'Invalid or expired JWT token'}), 401

@app_views.errorhandler(JWTExtendedException)
def handle_invalid_token_error(e):
    error_message = str(e)
    if "Expired" in error_message:
        return jsonify({'message': 'Expired token'}), 401
    elif "Invalid" in error_message:
        return jsonify({'message': 'Invalid token'}), 401
    else:
        return jsonify({'message': 'Invalid or expired token'}), 401

# Error handler for JWTExtendedException (base class for JWT exceptions)
@app_views.errorhandler(JWTExtendedException)
def handle_invalid_token_error(e):
    return jsonify({'message': 'Invalid or expired token'}), 401

# Error handler for ExpiredSignatureError (specific JWT exception)




@app_views.route('/client', methods=['POST'], strict_slashes=False)
#@jwt_required
@cross_origin()
def post_client():
    """create a new category"""
    verify_jwt_in_request()
    if not request.get_json():
        return make_response(jsonify(
            {'status': '401', 'message': 'The request data is empty'}), 400)
    
    obj:ObjectManagerInterface = ObjectManagerAdapter()  
    client = obj.add_object(
        Customer, **request.get_json())
    return make_response(jsonify(client.to_dict()), 201)


@app_views.route('/client/<string:client_id>', methods=['GET'], strict_slashes=False)
#@jwt_required
@cross_origin()
def get_client(client_id):
    """create a new client"""
    verify_jwt_in_request()
    print(client_id)
    customer: CustormPort = CustomerAdapter()
    customer_object = customer.find_object_by(Customer, **{"id":client_id})
    if customer_object is None:
        return make_response(jsonify(
            {'status': '401', 'message': 'No client is associated with this id'}), 404)
        
    return make_response(jsonify(customer_object), 200)

@app_views.route('/client_by_phone/<string:phone_number>', methods=['GET'], strict_slashes=False)
#@jwt_required
@cross_origin()
def get_client_by_phone(phone_number):
    """create a new client"""
    verify_jwt_in_request()
    print(phone_number)
    customer: CustormPort = CustomerAdapter()
    customer_object = customer.find_object_by(Customer, **{"phone_number":phone_number})
    print(customer_object)
    if customer_object is None:
        return make_response(jsonify(
            {'status': '404', 'message': 'No client is associated with this phone number.'}), 404)
    else:
        return make_response(jsonify(customer_object), 200)


@app_views.route('/clients_physique', methods=['GET'], strict_slashes=False)
#@jwt_required
@cross_origin()
def get_physiq_clients():
    """create a new client"""
    try:
        # Verify JWT in the request
        verify_jwt_in_request()
    except JWTExtendedException as e:
        # If verification fails, handle the exception
        return handle_jwt_error(e)
    #verify_jwt_in_request()
    customer: CustormPort = CustomerAdapter()
    kwarg = {"is_deleted": False, "customer_type_id":"c144bd80-fddd-4372-9836-833fa8f9d0c6"}
    customer_object = customer.find_all_client_data(Customer, **kwarg)
    page_obj = Paginator(customer_object)
    page = request.args.get('page', default=1, type=int)  # Get the page parameter from the request query string
    per_page = request.args.get('per_page', default=100, type=int)  # Get the per_page parameter from the request query string
    result = page_obj.get_hyper(page, per_page)
    return make_response(jsonify(result), 200)


@app_views.route('/clients_morale', methods=['GET'], strict_slashes=False)
#@jwt_required
@cross_origin()
def get_clients_morale():
    """create a new client"""
    customer: CustormPort = CustomerAdapter()
    kwarg = {"is_deleted": False, "customer_type_id":"f3604013-67cf-45ab-b2e7-ed39c1c59fec"}
    customer_object = customer.find_all_client_data(Customer, **kwarg)
    page_obj = Paginator(customer_object)
    page = request.args.get('page', default=1, type=int)  # Get the page parameter from the request query string
    per_page = request.args.get('per_page', default=100, type=int)  # Get the per_page parameter from the request query string
    result = page_obj.get_hyper(page, per_page)
    return make_response(jsonify(result), 200)



@app_views.route('/clients', methods=['GET'], strict_slashes=False)
#@jwt_required
@cross_origin()
def get_clients():
    """create a new client"""
    customer: CustormPort = CustomerAdapter()
    customer_object = customer.find_all_clients_data(Customer)
    page_obj = Paginator(customer_object)
    page = request.args.get('page', default=1, type=int)  # Get the page parameter from the request query string
    per_page = request.args.get('per_page', default=100, type=int)  # Get the per_page parameter from the request query string
    result = page_obj.get_hyper(page, per_page)
    return make_response(jsonify(result), 200)


@app_views.route('/customer', methods=['PUT'], strict_slashes=False)
@jwt_required()
@cross_origin()
def update_client():
    """create a new client"""
    if not request.get_json():
        return make_response(jsonify(
            {'status': '401', 'message': 'The request data is empty'}), 400)
    
    obj:ObjectManagerInterface = ObjectManagerAdapter()  
    obj.update_object_in_storage(
        Customer, request.get_json()["id"], **request.get_json())
    return make_response(jsonify({"message":"update made successfully", "status":200}), 200)

