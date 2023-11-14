from api.v1.endpoints import app_views
from flask_cors import cross_origin
from flask import abort, jsonify, make_response, request
from models.room_item import RoomItem
from services.room_service.room.adapter.room_item_adapter import RoomItemAdapter
from services.room_service.room.port.room_item_port import RoomItemPort


@app_views.route('/room_item', methods=['POST'], strict_slashes=False)
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
