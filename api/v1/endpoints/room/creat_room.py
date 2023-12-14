from api.v1.endpoints import app_views
from flask_cors import cross_origin
from flask import abort, jsonify, make_response, request
from models.room import Room
from services.room_service.room.port.room_port import RoomPort
from services.room_service.room.adapter.create_room_adapter import AddRoom


from services.object_manager_interface import ObjectManagerInterface
from services.room_service.room_category_manager.adapter.room_category_adapter import CreateCategoryRoom
@app_views.route('/room', methods=['POST'], strict_slashes=False)
@cross_origin()
def post_room():
    """create a new category"""
    if not request.get_json():
        return make_response(jsonify(
            {'status': '401', 'message': 'The request data is empty'}), 400)
        
    room_ob: RoomPort = AddRoom()
    
    room = room_ob.add_object(
        Room, **request.get_json())
    return make_response(jsonify(room.to_dict()), 201)

