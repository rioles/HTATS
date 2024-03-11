from api.v1.endpoints import app_views
from flask_cors import cross_origin
from flask import abort, jsonify, make_response, request
from models.room import Room
from models.room_item import RoomItem
from services.object_manager_adapter import ObjectManagerAdapter
from services.object_manager_interface import ObjectManagerInterface
from services.paginator import Paginator
from services.room_service.room.adapter.room_item_adapter import RoomItemAdapter
from services.room_service.room.port.room_item_port import RoomItemPort
from flask_jwt_extended import  jwt_required

@app_views.route('/room_item', methods=['POST'], strict_slashes=False)
#@jwt_required()
@cross_origin()
def post_room_item():
    """create a new category"""
    if not request.get_json():
        return make_response(jsonify(
            {'status': '401', 'message': 'The request data is empty'}), 400)
        
    room_ob: RoomItemPort = RoomItemAdapter()
    room = room_ob.add_object(
        RoomItem, **request.get_json())
    return make_response(jsonify(room), 201)



@app_views.route('/rooms', methods=['GET'], strict_slashes=False)
#@jwt_required()
@cross_origin()
def get_rooms():
    """create a new client"""
    room_ob: RoomItemPort = RoomItemAdapter()
    room_objects = room_ob.find_all_room_data(Room)
    page_obj = Paginator(room_objects)
    page = request.args.get('page', default=1, type=int)  # Get the page parameter from the request query string
    per_page = request.args.get('per_page', default=100, type=int)  # Get the per_page parameter from the request query string
    result = page_obj.get_hyper(page, per_page)
    return make_response(jsonify(result), 200)

@app_views.route('/room', methods=['PUT'], strict_slashes=False)
#@jwt_required()
@cross_origin()
def put_room():
    """create a new category"""
    if not request.get_json():
        return make_response(jsonify(
            {'status': '401', 'message': 'The request data is empty'}), 400)    
    obj:ObjectManagerInterface = ObjectManagerAdapter()
    obj.update_object_in_storage(Room, request.get_json()["id"], **request.get_json())
    room_obj = obj.find_object_by(Room, **{"id":request.get_json()["id"]})
    return make_response(jsonify(room_obj.to_dict()), 201)


@app_views.route('/room_item', methods=['PUT'], strict_slashes=False)
#@jwt_required()
@cross_origin()
def put_room_item():
    """create a new category"""
    if not request.get_json():
        return make_response(jsonify(
            {'status': '401', 'message': 'The request data is empty'}), 400)    
    obj:ObjectManagerInterface = ObjectManagerAdapter()
    obj.update_object_in_storage(RoomItem, request.get_json()["room_item_id"], **request.get_json())
    room_obj = obj.find_object_by(Room, **{"id":request.get_json()["room_item_id"]})
    return make_response(jsonify(room_obj.to_dict()), 201)



