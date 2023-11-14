from api.v1.endpoints import app_views
from flask_cors import cross_origin
from flask import abort, jsonify, make_response, request
from models.room import Room
from services.object_manager_adapter import ObjectManagerAdapter
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