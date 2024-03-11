from flask_cors import cross_origin
from api.v1.endpoints import app_views
from flask_jwt_extended import  jwt_required
from flask import abort, jsonify, make_response, request
from models.room_category import RoomCategory
from services.object_manager_adapter import ObjectManagerAdapter
from services.room_service.room_category_manager.port.room_category_interface import RoomCategoryPort
from services.paginator import Paginator
from services.object_manager_interface import ObjectManagerInterface
from services.room_service.room_category_manager.adapter.room_category_adapter import CreateCategoryRoom

@app_views.route('/room_category', methods=['POST'], strict_slashes=False)
#@jwt_required()
@cross_origin()
def post_room_category():
    """create a new category"""
    if not request.get_json():
        return make_response(jsonify(
            {'status': '401', 'message': 'The request data is empty'}), 400)
    category_registration: RoomCategoryPort = CreateCategoryRoom()
    
    category_room = category_registration.add_object(
        RoomCategory, **request.get_json())
    return make_response(jsonify(category_room.to_dict()), 201)

@app_views.route('/room_categories', methods=['GET'], strict_slashes=False)
#@jwt_required()
@cross_origin()
def get_room_categories():
    """get room categories information for all patients"""
    obj: ObjectManagerInterface = ObjectManagerAdapter()
    room_categories = obj.find_all(RoomCategory)
    print(room_categories)
    
    page_obj = Paginator(room_categories)
    page = request.args.get('page', default=1, type=int)  # Get the page parameter from the request query string
    per_page = request.args.get('per_page', default=10, type=int)  # Get the per_page parameter from the request query string
    result = page_obj.get_hyper(page, per_page)
    return jsonify(result)

@app_views.route('/room_categorie/<string:room_categorie_id>', methods=['GET'],
                 strict_slashes=False)
#@jwt_required()
@cross_origin()
def get_room_categorie(room_categorie_id : str):
    """get room category information for specified amenity"""
    room_categorie_obj = {}
    room_categorie_obj['id'] = room_categorie_id
    obj: ObjectManagerInterface = ObjectManagerAdapter()
    room_categorie = obj.find_object_by(RoomCategory, **room_categorie_obj)
    if room_categorie is None:
        abort(404)
    return jsonify(room_categorie.to_dict())

