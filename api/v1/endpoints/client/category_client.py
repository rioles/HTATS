from api.v1.endpoints import app_views
from flask import abort, jsonify, make_response, request
from models.customer_type import CustormerType
from services.paginator import Paginator
from services.room_service.room.port.room_port import RoomPort
from services.room_service.room.adapter.create_room_adapter import AddRoom
from services.object_manager_adapter import ObjectManagerAdapter
from services.object_manager_interface import ObjectManagerInterface
@app_views.route('/category_client', methods=['POST'], strict_slashes=False)
def post_category_client():
    """create a new category"""
    if not request.get_json():
        return make_response(jsonify(
            {'status': '401', 'message': 'The request data is empty'}), 400)
        
    obj: ObjectManagerInterface = ObjectManagerAdapter()
    custormer_type = obj.add_object(
        CustormerType, **request.get_json())
    return make_response(jsonify(custormer_type.to_dict()), 201)

@app_views.route('/categorie_client/<string:categorie_client_id>', methods=['GET'],
                 strict_slashes=False)
def get_category_client(categorie_client_id : str):
    """get room category information for specified amenity"""
    category_client_obj = {}
    category_client_obj['id'] = categorie_client_id
    obj: ObjectManagerInterface = ObjectManagerAdapter()
    category_client = obj.find_object_by(Customer, **category_client_obj)
    if category_client is None:
        abort(404)
    return jsonify(category_client.to_dict())

@app_views.route('/categories_clients', methods=['GET'], strict_slashes=False)
def get_categories_clients():
    """get room categories information for all patients"""
    obj: ObjectManagerInterface = ObjectManagerAdapter()
    categories_clients = obj.find_all(Customer)
    page_obj = Paginator(categories_clients)
    page = request.args.get('page', default=1, type=int)  # Get the page parameter from the request query string
    per_page = request.args.get('per_page', default=10, type=int)  # Get the per_page parameter from the request query string
    result = page_obj.get_hyper(page, per_page)
    return jsonify(result)


