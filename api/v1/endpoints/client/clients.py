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


from services.object_manager_interface import ObjectManagerInterface
from services.room_service.room_category_manager.adapter.room_category_adapter import CreateCategoryRoom
@app_views.route('/client', methods=['POST'], strict_slashes=False)
@cross_origin()
def post_client():
    """create a new category"""
    if not request.get_json():
        return make_response(jsonify(
            {'status': '401', 'message': 'The request data is empty'}), 400)
    
    obj:ObjectManagerInterface = ObjectManagerAdapter()  
    client = obj.add_object(
        Customer, **request.get_json())
    return make_response(jsonify(client.to_dict()), 201)


@app_views.route('/client/<string:client_id>', methods=['GET'], strict_slashes=False)
@cross_origin()
def get_client(client_id):
    """create a new client"""
    print(client_id)
    customer: CustormPort = CustomerAdapter()
    customer_object = customer.find_object_by(Customer, **{"id":client_id})
    if customer_object is None:
        return make_response(jsonify(
            {'status': '401', 'message': 'No client is associated with this id'}), 404)
        
    return make_response(jsonify(customer_object), 200)

@app_views.route('/client_by_phone/<string:phone_number>', methods=['GET'], strict_slashes=False)
@cross_origin()
def get_client_by_phone(phone_number):
    """create a new client"""
    print(phone_number)
    customer: CustormPort = CustomerAdapter()
    customer_object = customer.find_object_by(Customer, **{"phone_number":phone_number})
    if customer_object is None:
        return make_response(jsonify(
            {'status': '204', 'message': 'No client is associated with this phone number.'}), 204)
        
    return make_response(jsonify(customer_object), 200)


@app_views.route('/clients', methods=['GET'], strict_slashes=False)
@cross_origin()
def get_clients():
    """create a new client"""
    customer: CustormPort = CustomerAdapter()
    customer_object = customer.find_all_client_data(Customer)
    page_obj = Paginator(customer_object)
    page = request.args.get('page', default=1, type=int)  # Get the page parameter from the request query string
    per_page = request.args.get('per_page', default=10, type=int)  # Get the per_page parameter from the request query string
    result = page_obj.get_hyper(page, per_page)
    return make_response(jsonify(result), 200)





@app_views.route('/type_client', methods=['POST'], strict_slashes=False)
def post_type_client():
    """create a new category"""
    if not request.get_json():
        return make_response(jsonify(
            {'status': '401', 'message': 'The request data is empty'}), 400)
    
    obj:ObjectManagerInterface = ObjectManagerAdapter()  
    type_client = obj.add_object(
        CustormerType, **request.get_json())
    return make_response(jsonify(type_client.to_dict()), 201)